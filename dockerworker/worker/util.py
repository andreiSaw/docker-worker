import time

def multiple_replace(text, word_dict):
    for key, value in word_dict.items():
        text = text.replace(key, str(value))
    return text

def build_command(job):
    command = job.descriptor['cmd']
    command = multiple_replace(command, {
        "$OUTPUT_DIR": "/output",
        "$INPUT_DIR": "/input",
        "$JOB_ID": job.job_id,
        "$TIMESTAMP": time.time()
    })

    return command


def descriptor_correct(job):
    keys_needed = [
        ('cmd', unicode),
        ('cpu_per_container', int),
        ('max_memoryMB', int),
        ('min_memoryMB', int),
        ('env_container', dict)
    ]

    for key, keytype in keys_needed:
        assert isinstance(job.descriptor.get(key), keytype), "Error with key: " + key


def obtain_volumes(in_dir, out_dir, volumes):
    volumes_list = [
        "{}:/input".format(in_dir),
        "{}:/output".format(out_dir),
    ]

    volumes_list += volumes

    return volumes_list
