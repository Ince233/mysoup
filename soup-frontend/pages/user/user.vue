<template>
	<view class="userLayout pageBg">
		<!-- <custom-nav-bar title="我的"></custom-nav-bar> 还未定义-->
		<view class="userInfo">
			<view class="avatar">
				<image src="/static/images/mushroom2.png" mode="aspectFill"></image>
			</view>
			<view class="ip">100.100.100.100</view>
			<view class="address">来自：广东</view>
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
const clickContact = ()=>{
	uni.makePhoneCall(
	{
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
	.userInfo{
		display:flex;
		flex-direction:column;
		align-items:center;
		justify-content:center;
		width:100%;
		padding:40rpx 0;
		.avatar{
			width:100%;
			margin-bottom:20rpx;
			display:flex;
			align-items:center;
			justify-content:center;
			image{
				border-radius:80rpx;
				width:160rpx;
				height:160rpx;
			}
		}
		.ip{
			font-size:44rpx;
			color:$text-color-1;
			padding:20rpx 0 5rpx;
		}
		.address{
			font-size:28rpx;
			color:$text-color-2;
		}
	}
	.section{
		border:1px solid #eee;
		border-radius:10rpx;
		box-shadow: 0 0 3px 1px rgba(0,0,0,0.08);
		width:690rpx;
		margin: 50rpx auto;
		.list{
			.row{
				display: flex;
				justify-content: space-between;
				align-items: center;
				padding: 0 30rpx;
				height:100rpx;
				background-color: #fff;
				position: relative;
				&last-child{
					border-bottom:0;
				}
				.left{
					display:flex;
					align-items:center;
					:deep(){
						.uni-icons{
							color:$brand-theme-color !important;
						}
					}
					.text{
						color:$text-color-1;
						padding-left:10rpx;
					}
				}
				.right{
					display:flex;
					align-items:center;
					.text{
						color:#aaa;
					}
				}
				button{
					position: absolute;
					top: 0;
					left: 0;
					height: 100rpx;
					width: 100%;
					opacity:0;
				}
			}
		}
	}

</style>
