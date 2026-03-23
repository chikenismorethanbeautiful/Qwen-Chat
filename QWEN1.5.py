from modelscope import snapshot_download
model_dir = snapshot_download('qwen/Qwen2.5-0.5B-Instruct',
cache_dir='./')#cache_dir='./'为指定下载目录，不然会下载到C盘的缓存中