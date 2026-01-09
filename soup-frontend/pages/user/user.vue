<template>
	<view class="userLayout pageBg">
		<!-- <custom-nav-bar title="我的"></custom-nav-bar> 还未定义-->
		<view class="userInfo">
			<view class="avatar" @click="handleAvatarClick">
				<image :src="userInfo.avatar || '/static/images/starfish.png'" mode="aspectFill"></image>
			</view>
			<view class="ip">{{ userInfo.username || '点击头像登录' }}</view>
			<view class="address">来自：{{ userInfo.region || '未知' }}</view>
		</view>
		
				
		<view class="section">
			<view class="list">	
			
				<view class="row" @click="handleClick">
					<view class="left">
						<uni-icons type="list" size="26"></uni-icons>
						<view class="text">浏览记录</view>
					</view>
					<view class="right">
						<view class="text">33</view>
						<uni-icons type="right" size="15" color="#aaa"></uni-icons>
					</view>
				</view>
				<view class="row" @click="handleClick">
					<view class="left">
						<uni-icons type="star-filled" size="26"></uni-icons>
						<view class="text">我的收藏</view>
					</view>
					<view class="right">
						<view class="text">33</view>
						<uni-icons type="right" size="15" color="#aaa"></uni-icons>
					</view>
				</view>
				<view class="row" @click="handleClick">
					<view class="left">
						<uni-icons type="paperplane-filled" size="26"></uni-icons>
						<view class="text">我要投稿</view>
					</view>
					<view class="right">
						<view class="text">33</view>
						<uni-icons type="right" size="15" color="#aaa"></uni-icons>
					</view>
				</view>
				<view class="row" @click="handleClick">
					<view class="left">
						<uni-icons type="hand-up-filled" size="26"></uni-icons>
						<view class="text">分享小程序</view>
					</view>
					<view class="right">
						<view class="text">33</view>
						<uni-icons type="right" size="15" color="#aaa"></uni-icons>
					</view>
				</view>
				<view class="row" @click="handleClick">
					<view class="left">
						<uni-icons type="settings-filled" size="26"></uni-icons>
						<view class="text">设置</view>
					</view>
					<view class="right">
						<view class="text">33</view>
						<uni-icons type="right" size="15" color="#aaa"></uni-icons>
					</view>
				</view>
			</view>	
		</view>
		
		<view class="section">
			<view class="list">	
				<view class="row" >
					<view class="left">
						<uni-icons type="help-filled" size="26"></uni-icons>
						<view class="text">问题&反馈</view>
					</view>
					<view class="right">
						<view class="text">33</view>
						<uni-icons type="right" size="15" color="#aaa"></uni-icons>
					</view>
				</view>
				<view class="row" >
					<view class="left">
						<uni-icons type="contact-filled" size="26"></uni-icons>
						<view class="text">联系客服</view>
					</view>
					<view class="right">
						<view class="text">33</view>
						<uni-icons type="right" size="15" color="#aaa"></uni-icons>
					</view>
					<!-- #ifdef MP -->
						<button open-type="contact">联系客服</button>
					<!-- #endif -->
					<!-- #ifndef MP -->
						<button @click="clickContact">拨打电话</button>
					<!-- #endif -->				
				</view>
			</view>	
		</view>
		

	</view>
	
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { wechatLogin, getCurrentUser, isLoggedIn } from '../../utils/auth.js'

// 用户信息
const userInfo = ref({
	username: '',
	avatar: '',
	region: ''
})

// 页面加载时获取用户信息
onMounted(() => {
	loadUserInfo()
})

// 加载用户信息
const loadUserInfo = () => {
	if (isLoggedIn()) {
		const currentUser = getCurrentUser()
		if (currentUser) {
			userInfo.value = {
				username: currentUser.username || currentUser.nickName || '微信用户',
				avatar: currentUser.avatar || currentUser.avatarUrl || '',
				region: currentUser.region || ''
			}
		}
	}
}

// 点击头像处理函数
const handleAvatarClick = async () => {
	try {
		// 调用微信登录
		await wechatLogin()
		// 更新用户信息
		loadUserInfo()
		uni.showToast({
			title: '登录成功',
			icon: 'success'
		})
	} catch (error) {
		console.error('登录失败:', error)
		uni.showToast({
			title: '登录失败',
			icon: 'error'
		})
	}
}

const clickContact = ()=>{
	uni.makePhoneCall({
		phoneNumber:"18802245526"
	})
}

const handleClick = ()=>{
	uni.navigateTo({
		url:"/pages/classlist/classlist"
	})
}
</script>

<style lang="scss" scoped>
.userInfo {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	width: 100%;
	padding: 60rpx 0 50rpx;
	margin-bottom: 20rpx;
	
	.avatar {
		width: 160rpx;
		height: 160rpx;
		margin-bottom: 28rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(240, 248, 255, 0.9));
		box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.15);
		transition: all 0.4s ease;
		cursor: pointer;
		
		&:hover {
			transform: scale(1.05);
			box-shadow: 0 12rpx 32rpx rgba(0, 0, 0, 0.2);
		}
		
		image {
			border-radius: 50%;
			width: 152rpx;
			height: 152rpx;
		}
	}
	
	.ip {
		font-size: 44rpx;
		font-weight: 600;
		color: #333;
		padding: 10rpx 0;
		letter-spacing: 1rpx;
	}
	
	.address {
		font-size: 28rpx;
		color: #666;
		margin-top: 8rpx;
		background: rgba(255, 255, 255, 0.7);
		padding: 8rpx 24rpx;
		border-radius: 20rpx;
		backdrop-filter: blur(8px);
		border: 1rpx solid rgba(255, 255, 255, 0.5);
	}
}

.section {
	margin: 36rpx auto;
	width: 85vw;
	border-radius: 24rpx;
	box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.12);
	overflow: hidden;
	background: rgba(255, 255, 255, 0.85);
	backdrop-filter: blur(15px);
	border: 1rpx solid rgba(255, 255, 255, 0.5);
	
	.list {
		.row {
			display: flex;
			justify-content: space-between;
			align-items: center;
			padding: 0 40rpx;
			height: 110rpx;
			position: relative;
			transition: all 0.3s ease;
			cursor: pointer;
			
			&:hover {
				background: rgba(255, 255, 255, 0.95);
				transform: translateX(4rpx);
			}
			
			&:not(:last-child)::after {
				content: '';
				position: absolute;
				left: 40rpx;
				right: 40rpx;
				bottom: 0;
				height: 1rpx;
				background: linear-gradient(to right, transparent, rgba(200, 200, 200, 0.3), transparent);
			}
			
			.left {
				display: flex;
				align-items: center;
				
				:deep() {
					.uni-icons {
						color: #666 !important;
						font-size: 36rpx !important;
						margin-right: 24rpx;
					}
				}
				
				.text {
					color: #333;
					font-size: 32rpx;
					font-weight: 500;
				}
			}
			
			.right {
				display: flex;
				align-items: center;
				gap: 16rpx;
				
				.text {
					color: #999;
					font-size: 28rpx;
				}
				
				:deep() {
					.uni-icons {
						color: #ccc !important;
						font-size: 20rpx !important;
					}
				}
			}
			
			button {
				position: absolute;
				top: 0;
				left: 0;
				height: 100%;
				width: 100%;
				opacity: 0;
			}
		}
	}
}

/* 为第一个section添加特殊样式 */
.section:first-of-type {
	margin-top: 0;
}

/* 为最后一个section添加特殊样式 */
.section:last-of-type {
	margin-bottom: 60rpx;
}
</style>
