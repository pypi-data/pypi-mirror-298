from .dataset import EvotuneDataset
from .transform import TokenizeAndMask
import os
from transformers import AutoTokenizer, EsmForMaskedLM, Trainer, TrainingArguments, TrainerCallback
from peft import get_peft_model, LoraConfig, TaskType
import torch
from accelerate import Accelerator
from pynvml import (nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex,
                    nvmlDeviceGetMemoryInfo, nvmlShutdown)


class GpuUtilizationCallback(TrainerCallback):

    def on_step_end(self, args, state, control, **kwargs):

        # log selected batch size
        if args.auto_find_batch_size:
            print("Selected Batch Size: ", args.train_batch_size,
                  "Per Device: ", args.per_device_train_batch_size)

        if torch.cuda.is_available():
            self.print_gpu_utilization()

    def print_gpu_utilization(self):
        nvmlInit()
        deviceCount = nvmlDeviceGetCount()
        for i in range(deviceCount):
            handle = nvmlDeviceGetHandleByIndex(i)
            info = nvmlDeviceGetMemoryInfo(handle)
            print("Device {}: Memory Total: {} MB, Memory Used: {} MB".format(
                i, info.total / 1024 / 1024, info.used / 1024 / 1024))
        nvmlShutdown()


class MyTrainer(Trainer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def compute_loss(self, model, inputs, return_outputs=False):
        outputs = model(**inputs)
        loss = outputs.loss.mean()
        outputs["loss"] = loss
        return (loss, outputs) if return_outputs else loss


def train(data, model_path, max_length, epochs,
          batch_size, target_fasta, output_dir, take,
          eval, tokenizer, save_total_limit, cache_dir, max_evalue, lora=False):

    # load dataset
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer, cache_dir=cache_dir, clean_up_tokenization_spaces=True)
    transform = TokenizeAndMask(tokenizer, max_length)
    train_dataset, test_dataset = EvotuneDataset(
        data, target_fasta, max_evalue, transform=transform,
        take=take).train_test_split(test_size=0.2)

    # get accelerator
    accelerator = Accelerator()

    # get model and according tokenizer
    model = EsmForMaskedLM.from_pretrained(model_path, cache_dir=cache_dir)

    if lora:
        print("Using LORA")
        peft_config = LoraConfig(
            task_type=TaskType.TOKEN_CLS,
            inference_mode=False,
            r=2,
            lora_alpha=1,
            target_modules=["query", "key", "value"],
            bias="none",
            lora_dropout=0.2
        )
        model = get_peft_model(model, peft_config)

    model, train_dataset, test_dataset = accelerator.prepare(
        model, train_dataset, test_dataset)

    # get the device the model is on
    print("Model is on device: ", model.device)
    print("Data on device", train_dataset[0]['input_ids'].device)
    print("Samples in Train Dataset: ", len(train_dataset))
    print("Samples in Test Dataset: ", len(test_dataset))
    print("Sample shape: ", train_dataset[0]['input_ids'].shape)

    print("auto_find_batch_size is enabled. starting with batch size: ", batch_size)

    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        auto_find_batch_size=True,
        save_total_limit=save_total_limit,
        save_strategy=eval,
        eval_strategy=eval,
        logging_steps=2,
        logging_dir=os.path.join(output_dir, "logs"),
        report_to="tensorboard",
        metric_for_best_model="eval_loss",
        load_best_model_at_end=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        callbacks=[GpuUtilizationCallback()],
    )

    accelerator.prepare(trainer)

    if os.path.exists(model_path):
        trainer.train(resume_from_checkpoint=model_path)
    else:
        trainer.train()






