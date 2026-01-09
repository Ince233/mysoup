<template>
	<view class="discoverLayout pageBg">
		<view class="search">
			<navigator url="/pages/search/search">
				<view class="searchBox">
					<view class="icon">
						<uni-icons type="search" size="20" color="#7d7d7d"></uni-icons>
					</view>
					<view class="text">
						搜索
					</view>
				</view>
			</navigator>
		</view>
		<view class="classify">
			<view class="title">专题分类</view>
			<view class="content">
				<view
					class="classes"
					v-for="(item, index) in iconTextList"
					:key="index"
					@click="updateList(item.text)"
				>
					<view class="icon">
						<uni-icons :type="item.icon" size="30" color="$text-color-1"></uni-icons>
					</view>
					<view class="text">
						{{item.text}}
					</view>
				</view>
			</view>
		</view>
		<view class="notice">
			<view class="left">
				<uni-icons type="sound" size="20"></uni-icons>
				<text class="text">公告</text>
			</view>
			<view class="center">
				<swiper vertical autoplay interval="1500" duration="300" circular>
					<swiper-item>欢迎使用海龟汤小程序，点击扫码关注</swiper-item>
					<swiper-item>海龟汤小程序，版权公告</swiper-item>
				</swiper>
			</view>
			<view class="right">
				<uni-icons type="forward" size="16" color="#333"></uni-icons>
			</view>
		</view>
		<view class="recommend">
			<view class="title">每日推荐</view>
			<view class="list" v-for="(item, index) in thisSoupList" :key="item.id">
				<uni-card
					@click="goToDetail(item.id)"
					:title="item.title"
					:extra="item.tag"
					:is-shadow="true"
					shadow="0px 0px 3px 1px rgba(0, 0, 0, 0.08)"
				>
					<text class="uni-body">{{ item.riddle }}</text>
				</uni-card>
			</view>
		</view>
	</view>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import soupList from '@/static/soupText/soupInfo.json'

// 当前展示的汤列表
const thisSoupList = ref([])

// 初始化：随机推荐 5 道汤
const initRandomSoupList = () => {
	const usedIndex = new Set()
	const result = []
	const total = soupList.length

	while (result.length < 5 && usedIndex.size < total) {
		const randomIndex = Math.floor(Math.random() * total)
		if (!usedIndex.has(randomIndex)) {
			usedIndex.add(randomIndex)
			result.push(soupList[randomIndex])
		}
	}

	thisSoupList.value = result
}

onBeforeMount(() => {
	initRandomSoupList()
})
//分类板块图标
const iconTextList = [
      { icon: 'color-filled', text: '入门' },
      { icon: 'eye-filled', text: '惊悚' },
      { icon: 'heart-filled', text: '情感' },
      { icon: 'notification-filled', text: '脑洞' },
      { icon: 'staff-filled', text: '职场' },
      { icon: 'gift-filled', text: '校园' },
      { icon: 'map-filled', text: '古风' },
      { icon: 'more-filled', text: '其他' }
    ]
//跳转到详情页
const goToDetail = (id) => {
	uni.navigateTo({
		url:'/pages/soupDetail/soupDetail?id=' + id
	})
}
//根据分类更新展示列表
//thisSoupList

const _deprecatedUpdateList = ()  => {
	
	soupList
	thisSoupList = updatedList
}

// 根据分类更新展示列表（点击分类时触发）
const updateList = (category)  => {
	// 按 tag 精确匹配分类
	const filtered = soupList.filter(item => item.tag === category)

	// 如果该分类下数量很多，只取前 5 条
	if (filtered.length > 0) {
		thisSoupList.value = filtered.slice(0, 5)
	} else {
		// 如果没有匹配结果，回退到随机推荐
		initRandomSoupList()
	}
}
</script>

<style lang="scss" scoped>
.discoverLayout{
	padding-bottom: 40rpx;
	
	.search{
		margin: 40rpx auto 20rpx;
		width: 88vw;
		height:100rpx;
		border-radius:50rpx;
		background: rgba(255, 255, 255, 0.9);
		backdrop-filter: blur(10px);
		display:flex;
		justify-content:center;
		align-items:center;
		box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.1);
		transition: all 0.3s ease;
		
		&:hover {
			box-shadow: 0 6rpx 25rpx rgba(0, 0, 0, 0.15);
		}
		
		.searchBox{
			display:flex;
			justify-content: center;
			align-items:center;
			text-decoration: none;
			
			.text{
				color:#666;
				padding-left:16rpx;
				font-size: 32rpx;
			}
		}
	}
	
	.classify{
		display:flex;
		flex-direction:column;
		padding:0 40rpx 20rpx;
		
		.title{
			font-size:38rpx;
			font-weight: 600;
			margin:30rpx 0;
			color:#333;
			padding-left:10rpx;
			border-left: 6rpx solid #a0c6c5;
		}
		
		.content{
			display:grid;
			grid-template-columns: repeat(4,1fr);
			gap:24rpx;
			
			.classes{
				display:flex;
				flex-direction:column;
				align-items:center;
				justify-content: center;
				padding:20rpx 10rpx;
				border-radius:16rpx;
				background: rgba(255, 255, 255, 0.85);
				backdrop-filter: blur(5px);
				transition: all 0.3s ease;
				cursor: pointer;
				
				&:hover {
					transform: translateY(-4rpx);
					box-shadow: 0 8rpx 25rpx rgba(0, 0, 0, 0.12);
				}
				
				:deep(){
					.uni-icons {
						color:#a0c6c5 !important;
						font-weight: bold;
					}
				}
				
				.text{
					padding-top:12rpx;
					color:#444;
					font-size: 28rpx;
					font-weight: 500;
				}
			}
		}
	}
	
	.notice{
		width: 88vw;
		height: 90rpx;
		line-height:90rpx;
		background: rgba(255, 255, 255, 0.9);
		backdrop-filter: blur(10px);
		margin: 0 auto 30rpx;
		border-radius: 45rpx;
		display:flex;
		align-items: center;
		box-shadow: 0 4rpx 15rpx rgba(0, 0, 0, 0.08);
		
		.left{
			width:120rpx;
			display:flex;
			align-items:center;
			justify-content:center;
			
			:deep(){
				.uni-icons{
					color:#d1e4a3 !important;
					font-weight: bold;
				}
			}
			
			.text{
				color:#333;
				font-weight:bold;
				font-size:30rpx;
				margin-left:8rpx;
			}
		}
		
		.center{
			flex:1;
			swiper{
				height:100%;
				
				&-item{
					height:100%;
					font-size: 32rpx;
					color:#666;
					overflow:hidden;
					white-space:nowrap;
					text-overflow:ellipsis;
				}
			}
		}
		
		.right{
			width:60rpx;
			display:flex;
			align-items:center;
			justify-content:center;
			
			:deep() {
				.uni-icons {
					color:#ccc;
				}
			}
		}
	}
	
	.recommend{
		display:flex;
		flex-direction:column;
		padding:0 40rpx;
		
		.title{
			font-size:38rpx;
			font-weight: 600;
			margin:0 0 20rpx;
			color:#333;
			padding-left:10rpx;
			border-left: 6rpx solid #d1e4a3;
		}
		
		:deep(){
			.uni-card {
				margin-bottom: 24rpx;
				border-radius: 20rpx;
				background: rgba(255, 255, 255, 0.95);
				backdrop-filter: blur(10px);
				box-shadow: 0 6rpx 20rpx rgba(0, 0, 0, 0.08);
				transition: all 0.3s ease;
				
				&:hover {
					transform: translateY(-2rpx);
					box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.12);
				}
				
				.uni-card__header {
					border-bottom: 2rpx solid #f0f0f0;
					padding: 24rpx 30rpx;
					
					.uni-card__title {
						font-size: 34rpx;
						font-weight: 600;
						color: #333;
					}
					
					.uni-card__extra {
						font-size: 26rpx;
						color: #a0c6c5;
						background: rgba(160, 198, 197, 0.1);
						padding: 4rpx 16rpx;
						border-radius: 12rpx;
					}
				}
				
				.uni-card__content {
					padding: 30rpx;
					
					.uni-body {
						font-size: 30rpx;
						color: #666;
						line-height: 1.6;
					}
				}
			}
		}
	}
}
</style>
