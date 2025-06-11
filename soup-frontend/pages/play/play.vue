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
@mixin button($thisWidth){
	margin:auto;
	width:$thisWidth;
	height:100rpx;
	display:flex;
	justify-content: center;
	align-items:center;
	background-color: #fff;
	border-radius:50rpx;
	opacity: 0.8;
	border: 1rpx solid #a6a6a6;
	.text{
		padding-left:20rpx;
	}
}	
.playLayout{
	overflow:hidden;
	display:flex;
	flex-direction:column;
	min-height:90vh;
	.buttonWrapper{
		height:25vh;
		display:flex;
		flex-direction: column;
		.quickPlay{
			@include button(85vw);
		}
		.createRoom{
			@include button(85vw);
			margin-bottom:40rpx;
		}
		.search{
			margin:0 30rpx;
			display:flex;
			justify-content: center;
			.searchRoom{
			@include button(60vw);
			}
			.filterButton{
			@include button(20vw);
			}
		}
	}

	.roomList{
		display:flex;
		flex-direction:column;
		padding:20rpx 40rpx;
	}
}      
</style>
