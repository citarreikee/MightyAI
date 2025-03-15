from huggingface_hub import snapshot_download

# repo_id = "ziqingyang/chinese-alpaca-lora-7b"
repo_id = "sentence-transformers/all-MiniLM-L6-v2"
local_dir = './models'
cache_dir = local_dir + "/cache"
while True:
    try:
        snapshot_download(cache_dir=cache_dir,
        local_dir=local_dir,
        repo_id=repo_id,
        local_dir_use_symlinks=False, # 不转为缓存乱码的形式, auto, Small files (<5MB) are duplicated in `local_dir` while a symlink is created for bigger files.
        resume_download=True,
        allow_patterns=["*.model", "*.json", "*.bin",
        "*.py", "*.md", "*.txt"],
        ignore_patterns=["*.safetensors", "*.msgpack",
        "*.h5", "*.ot", ],
        )
    except Exception as e :
        print(e)
