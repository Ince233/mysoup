<template>
	<view class="container pageBg">
		<view class="chat-container">
			<scroll-view 
				scroll-y="true" 
				class="chat-list" 
				:scroll-top="scrollTop"
				:scroll-with-animation="true"
				:show-scrollbar="false"
				@scroll="handleScroll"
			>
				<view class="chat-list-inner">
					<view v-for="(message, index) in messages" :key="index" class="message-item" :class="message.role">
						<image 
							:src="message.role === 'assistant' ? '/static/images/mushroom.png' : '/static/images/mushroom.png'"
							class="avatar"
							mode="aspectFill"
						/>
						<view class="message-content">
							<text>{{ message.content }}</text>
						</view>
					</view>
				</view>
			</scroll-view>
			
			<view class="input-container">
				<input 
					type="text" 
					v-model="inputMessage" 
					placeholder="请输入你的问题..." 
					@confirm="sendMessage"
					class="input-box"
				/>
				<button @tap="sendMessage" class="send-btn">发送</button>
			</view>
		</view>
	</view>
</template>

<script>
	// 节流函数
	function throttle(fn, delay) {
		let last = 0;
		return function (...args) {
			const now = Date.now();
			if (now - last > delay) {
				last = now;
				fn.apply(this, args);
			}
		}
	}

	export default {
		data() {
			return {
				messages: [],
				inputMessage: '',
				scrollTop: 0,
				apiUrl: 'http://127.0.0.1:5000/api/chat',
				isScrolling: false
			}
		},
		onLoad() {
			// 添加欢迎消息
			this.messages.push({
				role: 'assistant',
				content: '欢迎来到海龟汤推理剧场！我是你的主持人小汤。\n\n在这里，每个故事都是一碗待你品尝的"谜之汤"—— 我会给你一个看似离奇的「汤面」（故事片段）， 而你，需要通过「是/否」提问，一步步揭开「汤底」（真相）。\n\n规则很简单：\n1️⃣ 我只能回答【是】、【否】或【无关】\n2️⃣ 大胆假设，小心求证，脑洞越大越好！\n3️⃣ 如果卡住，随时可以申请提示~\n\n准备好了吗？让我们开始第一道汤——'
			});
		},
		methods: {
			// 使用节流处理滚动事件
			handleScroll: throttle(function(e) {
				this.isScrolling = true;
				setTimeout(() => {
					this.isScrolling = false;
				}, 150);
			}, 100),

			async sendMessage() {
				if (!this.inputMessage.trim()) return;
				
				// 添加用户消息
				this.messages.push({
					role: 'user',
					content: this.inputMessage
				});
				
				const userMessage = this.inputMessage;
				this.inputMessage = '';
				this.scrollToBottom();
				
				try {
					const response = await uni.request({
						url: this.apiUrl,
						method: 'POST',
						header: {
							'content-type': 'application/json'
						},
						data: {
							messages: this.messages
						}
					});
					
					console.log('API Response:', response);
					
					if (response.statusCode === 200 && response.data && response.data.content) {
						// 添加AI回复，移除开头的空白字符
						this.messages.push({
							role: 'assistant',
							content: response.data.content.trim()
						});
						this.scrollToBottom();
					} else {
						throw new Error('Invalid response format');
					}
				} catch (error) {
					console.error('Error:', error);
					uni.showToast({
						title: '发送失败，请重试',
						icon: 'none',
						duration: 2000
					});
					
					// 添加错误提示消息
					this.messages.push({
						role: 'assistant',
						content: '抱歉，我遇到了一些问题，请稍后再试。'
					});
					this.scrollToBottom();
				}
			},
			scrollToBottom() {
				if (this.isScrolling) return;
				
				// 使用 nextTick 确保在 DOM 更新后滚动
				this.$nextTick(() => {
					setTimeout(() => {
						const query = uni.createSelectorQuery().in(this);
						query.select('.chat-list').boundingClientRect(data => {
							if (data) {
								this.scrollTop = data.height;
							}
						}).exec();
					}, 100);
				});
			}
		}
	}
</script>

<style lang="scss" scoped>
.container {
	padding: 0;
	height: 100vh;
	box-sizing: border-box;
}

.chat-container {
	display: flex;
	flex-direction: column;
	height: 100%;
	position: relative;

}

.chat-list {
	flex: 1;

}

.chat-list-inner {
	padding: 20rpx 10rpx;
	padding-bottom: 180rpx;
}

.message-item {
	margin-bottom: 20rpx;
	display: flex;
	align-items: flex-start;
	padding-right: 20rpx;
	transform: translateZ(0); /* 开启硬件加速 */
}

.message-item.user {
	flex-direction: row-reverse;
}

.message-item.assistant {
	flex-direction: row;
}

.avatar {
	width: 80rpx;
	height: 80rpx;
	border-radius: 50%;
	margin: 0 10rpx;
	flex-shrink: 0;
}

.message-content {
	max-width: calc(85% - 100rpx);
	padding: 20rpx;
	border-radius: 10rpx;
	word-break: break-all;
	white-space: pre-wrap;
	line-height: 1.5;
}

.message-content text {
	display: block;
}

.user .message-content {
	background-color: $brand-theme-color;
	color: white;
}

.assistant .message-content {
	background-color: white;
	color: #333;
}

.input-container {
	position: fixed;
	left: 0;
	right: 0;
	bottom: 90rpx;
	padding: 20rpx;
	background-color: white;
	display: flex;
	align-items: center;
	border-top: 1rpx solid #eee;
	z-index: 100;
}

.input-box {
	flex: 1;
	height: 80rpx;
	background-color: #f5f5f5;
	border-radius: 40rpx;
	padding: 0 30rpx;
	margin-right: 20rpx;
}

.send-btn {
	width: 120rpx;
	height: 80rpx;
	background-color: $brand-theme-color;
	color: white;
	border-radius: 40rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 28rpx;
}
</style>
