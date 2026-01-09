<template>
	<view class="playLayout pageBg">
		<view class="buttonWrapper">
			<view class="quickPlay">
				<uni-icons type="plusempty" size="20"></uni-icons>
				<view class="text">快速加入</view>
			</view>
			
			<view class="createRoom">
				<uni-icons type="plus" size="20"></uni-icons>
				<view class="text">创建房间</view>
			</view>
			
			<view class="search">
				<view class="searchRoom">
					<uni-icons type="search" size="20"></uni-icons>
					<view class="text">搜索房间</view>
				</view>
				<view class="filterButton">
					<uni-icons type="tune" size="20"></uni-icons>
					<view class="text">筛选</view>
				</view>
			</view>
		</view>

		
		<view class="roomList">
			<view class="list" v-for="item in 8" :key="item.index">
				<uni-card :title="`房间${item}`" extra="tag" :is-shadow="true" shadow="0px 0px 3px 1px rgba(0, 0, 0, 0.08)">
					<text class="uni-body">userName的房间</text>
				</uni-card>
			</view>
		</view>
		
	</view>
</template>

<script setup>
	
</script>

<style lang="scss" scoped>
@mixin button($thisWidth, $bgColor: rgba(255, 255, 255, 0.9)) {
	margin: auto;
	width: $thisWidth;
	height: 100rpx;
	display: flex;
	justify-content: center;
	align-items: center;
	background-color: $bgColor;
	border-radius: 50rpx;
	box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.12);
	backdrop-filter: blur(10px);
	transition: all 0.3s ease;
	border: 1rpx solid rgba(255, 255, 255, 0.5);
	
	&:hover {
		transform: translateY(-2rpx);
		box-shadow: 0 12rpx 28rpx rgba(0, 0, 0, 0.18);
	}
	
	&:active {
		transform: translateY(0);
	}
	
	.text {
		padding-left: 20rpx;
		font-size: 32rpx;
		font-weight: 500;
		color: #333;
	}
	
	.uni-icons {
		color: #666;
	}
}	

.playLayout {
	overflow: hidden;
	display: flex;
	flex-direction: column;
	min-height: 100vh;
	padding: 20rpx 0;
	
	.buttonWrapper {
		height: 28vh;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		gap: 30rpx;
		
		.quickPlay {
			@include button(85vw);
			background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(240, 248, 255, 0.95));
		}
		
		.createRoom {
			@include button(85vw);
			background: linear-gradient(135deg, rgba(248, 249, 250, 0.95), rgba(233, 236, 239, 0.95));
		}
		
		.search {
			width: 85vw;
			display: flex;
			gap: 20rpx;
			
			.searchRoom {
				@include button(65%);
				background: rgba(255, 255, 255, 0.9);
				
				.uni-icons {
					color: #999;
				}
				
				.text {
					color: #999;
					font-weight: 400;
				}
			}
			
			.filterButton {
				@include button(25%);
				background: rgba(255, 255, 255, 0.9);
			}
		}
	}

	.roomList {
		display: flex;
		flex-direction: column;
		padding: 0 30rpx;
		gap: 20rpx;
		
		.list {
			:deep() {
				.uni-card {
					background: rgba(255, 255, 255, 0.9);
					backdrop-filter: blur(10px);
					border-radius: 24rpx;
					box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
					border: none;
					transition: all 0.3s ease;
					
					&:hover {
						transform: translateY(-4rpx);
						box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.12);
					}
					
					.uni-card-header {
						padding: 24rpx 28rpx;
						border-bottom: 1rpx solid rgba(0, 0, 0, 0.06);
						
						.uni-card-header-title {
							font-size: 34rpx;
							font-weight: 600;
							color: #333;
						}
						
						.uni-card-header-extra {
							font-size: 26rpx;
							color: #666;
							background: rgba(240, 240, 240, 0.8);
							padding: 8rpx 16rpx;
							border-radius: 16rpx;
						}
					}
					
					.uni-card-content {
						padding: 24rpx 28rpx;
						
						.uni-body {
							font-size: 28rpx;
							color: #666;
						}
					}
				}
			}
		}
	}
}
</style>
