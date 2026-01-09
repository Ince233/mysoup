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
							:src="message.role === 'assistant' ? '/static/images/turtle.png' : '/static/images/jellyfish.png'"
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
	padding: 20rpx 20rpx 180rpx;
}

.message-item {
	margin-bottom: 28rpx;
	display: flex;
	align-items: flex-end;
	transform: translateZ(0); /* 开启硬件加速 */
	
	&:last-child {
		margin-bottom: 0;
	}
}

.message-item.user {
	flex-direction: row-reverse;
	padding-left: 40rpx;
}

.message-item.assistant {
	flex-direction: row;
	padding-right: 40rpx;
}

.avatar {
	width: 80rpx;
	height: 80rpx;
	border-radius: 50%;
	margin: 0 16rpx;
	flex-shrink: 0;
	box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.15);
	transition: transform 0.3s ease;
	
	&:hover {
		transform: scale(1.05);
	}
}

.message-content {
	max-width: calc(85% - 120rpx);
	padding: 24rpx 32rpx;
	word-break: break-all;
	white-space: pre-wrap;
	line-height: 1.6;
	font-size: 30rpx;
	position: relative;
	
	&::before {
		content: '';
		position: absolute;
		bottom: 24rpx;
		width: 0;
		height: 0;
		border-style: solid;
	}
}

.user .message-content {
	background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(240, 248, 255, 0.95));
	color: #333;
	border-radius: 28rpx 8rpx 28rpx 28rpx;
	box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.12);
	backdrop-filter: blur(10px);
	border: 1rpx solid rgba(255, 255, 255, 0.5);
	
	&::before {
		right: -20rpx;
		border-width: 12rpx 0 12rpx 20rpx;
		border-color: transparent transparent transparent rgba(255, 255, 255, 0.95);
	}
}

.assistant .message-content {
	background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 249, 250, 0.95));
	color: #333;
	border-radius: 8rpx 28rpx 28rpx 28rpx;
	box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.12);
	backdrop-filter: blur(10px);
	border: 1rpx solid rgba(255, 255, 255, 0.5);
	
	&::before {
		left: -20rpx;
		border-width: 12rpx 20rpx 12rpx 0;
		border-color: transparent rgba(255, 255, 255, 0.95) transparent transparent;
	}
}

.message-content text {
	display: block;
}

.input-container {
	position: fixed;
	left: 0;
	right: 0;
	bottom: 90rpx;
	padding: 20rpx 30rpx;
	display: flex;
	align-items: center;
	z-index: 100;
	
	&::before {
		content: '';
		position: absolute;
		left: 0;
		right: 0;
		top: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.85);
		backdrop-filter: blur(20px);
		border-top: 1rpx solid rgba(255, 255, 255, 0.5);
		border-bottom: 1rpx solid rgba(255, 255, 255, 0.5);
		box-shadow: 0 -4rpx 24rpx rgba(0, 0, 0, 0.08);
		z-index: -1;
	}
}

.input-box {
	flex: 1;
	height: 90rpx;
	background: rgba(255, 255, 255, 0.9);
	border-radius: 45rpx;
	padding: 0 40rpx;
	margin-right: 24rpx;
	font-size: 30rpx;
	color: #333;
	border: 1rpx solid rgba(200, 200, 200, 0.3);
	box-shadow: inset 0 2rpx 8rpx rgba(0, 0, 0, 0.06);
	transition: all 0.3s ease;
	
	&:focus {
		outline: none;
		border-color: rgba(200, 200, 200, 0.6);
		box-shadow: inset 0 2rpx 12rpx rgba(0, 0, 0, 0.1);
	}
	
	&::placeholder {
		color: #999;
		font-size: 28rpx;
	}
}

.send-btn {
	width: 130rpx;
	height: 90rpx;
	background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(240, 248, 255, 0.95));
	color: #333;
	border-radius: 45rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 30rpx;
	font-weight: 500;
	box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.12);
	border: 1rpx solid rgba(255, 255, 255, 0.5);
	transition: all 0.3s ease;
	
	&:hover {
		transform: translateY(-2rpx);
		box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.18);
	}
	
	&:active {
		transform: translateY(0);
	}
}
</style>
