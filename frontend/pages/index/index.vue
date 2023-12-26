<template>
	<view class="content">
		<text>制作你的声音</text>
		<input type="file" id="fileInput" accept=".wav" @change="onFileChange" />
		<input type='text' v-model='audio_name' placeholder="请输入名称" />
		<button @click="uploadFile">上传文件</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				selectFile: null,
				audio_name: ''
			}
		},
		onLoad() {

		},
		methods: {
			onFileChange(event) {
				const files = event.target.files;
				if (files.length > 0)
					this.selectFile = files[0];
			},
			uploadFile() {
				if (!this.selectFile) {
					uni.showToast({
						title: '请选择一个音频文件',
						icon: 'none'
					});
					return;
				}

				const formData = new FormData();
				formData.append('audio_file', this.selectedFile);
				formData.append('file_name', this.fileName.trim() + '.wav'); // 发送文件名
				formData.append('type', 2);

				uni.uploadFile({
					url: 'http://127.0.0.1:5000/upload',
					name: 'file',
					formData: formData,
					success: uploadRes => {
						console.log('上传成功', uploadRes);
					},
					fail: uploadErr => {
						console.error('上传失败', uploadErr);
					}
				})
			}
		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
</style>