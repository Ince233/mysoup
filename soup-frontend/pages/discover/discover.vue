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
				<view class="classes"  v-for="(item, index) in iconTextList" :key="index">
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
			<view class="list" v-for="(item, index) in randomSoup" :key="item.id">
				<uni-card @click="goToDetail(item.id)":title="item.title" :extra="item.tag" :is-shadow="true" shadow="0px 0px 3px 1px rgba(0, 0, 0, 0.08)">
					<text class="uni-body">{{ item.riddle }}</text>
				</uni-card>
			</view>
		</view>
	</view>
</template>

<script setup>
import {ref} from 'vue'
import soupList from '@/static/soupText/soupInfo.json'

//获取本地海龟汤
//console.log(soupList)  // 你可以直接使用这个对象
let randomSoup = ref([])
for(let i = 0 ; i < 8; i++){
	let randomIndex = Math.floor(Math.random()*24)
	if(!randomSoup.value.includes(soupList[randomIndex])){
		randomSoup.value.push(soupList[randomIndex])
	}
}
//console.log(randomSoup)
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
</script>

<style lang="scss" scoped>
.discoverLayout{
	overflow:hidden;//解决外边距塌陷
	.search{
		margin: 40rpx auto;
		margin-bottom:0;
		width: 85vw;
		height:100rpx;
		border-radius:50rpx;
		border: 1rpx solid #a6a6a6;
		display:flex;
		justify-content:center;
		align-items:center;
		background-color: #fff;
		opacity:0.8;
		.searchBox{
			display:flex;
			justify-content: center;
			align-items:center;
			.text{
				color:$text-color-2;
				padding-left:20rpx;
			}
		}
	}
	.classify{
		display:flex;
		flex-direction:column;
		padding:20rpx 40rpx;
		margin-bottom:20rpx;
		.title{
			font-size:35rpx;
			margin:30rpx auto;
			color:$text-color-1;
		}
		.content{
			display:grid;
			grid-template-columns: repeat(4,1fr);
			gap:40rpx;
			.classes{
				display:flex;
				flex-direction:column;
				align-items:center;
				justify-content: space-between;
				:deep(){
					.uni-icons {
						color:$text-color-1 !important;
					}
				}
				.text{
					padding-top:15rpx;
					color:$text-color-1;
				}
			}
		}
	}
	.notice{
		width: 85vw;
		height: 80rpx;
		line-height:80rpx;
		background: #fff;
		opacity: 0.8;
		margin: 0 auto;
		border: 1rpx solid #a6a6a6;
		border-radius: 40rpx;
		display:flex;
		.left{
			width:140rpx;
			display:flex;
			align-items:center;
			justify-content:center;
			:deep(){
				.uni-icons{
					color:$brand-theme-color !important;
				}
			}
			.text{
				color:$text-color-1;
				font-weight:bold;
				font-size:28rpx;
			}
	
		}
		.center{
			flex:1;
			swiper{
				height:100%;
				&-item{
					height:100%;
					font-size: 30rpx;
					color:$text-color-2;
					overflow:hidden;
					white-space:nowrap;
					text-overflow:ellipsis;
				}
			}
		}
		.right{
			width:70rpx;
			display:flex;
			align-items:center;
			justify-content:center;
		}
	}
	.recommend{
		display:flex;
		flex-direction:column;
		padding:20rpx 40rpx;
		.title{
			font-size:35rpx;
			margin:30rpx auto;
			color:$text-color-1;
		}
		:deep(){
			.unicard{
				background-color: #a0c6c5 !important;//没起作用
			}
		}
	}
}
</style>
