<template>
	<view class="soupDetailLayout pageBg">
		<view class="head">
			<!-- 这里展示头像，用户名和标题 -->
			<view class="avatar">
				<image src="/static/images/crab.png" mode="aspectFit"></image>
				<view class="userInfo">
					<view class="userName">测试用户1</view>
					<view class="userId">uid:000001</view>
				</view>
			</view>
			<view class="soupInfo">
				<view class="title">{{thisSoup.title}}</view>
				<view class="tag">#{{thisSoup.tag}}</view>
			</view>
		</view>
		
		<view class="body">
			<!-- 这里展示汤底和汤面 -->
			<view class="riddle">
				<uni-card title="汤底" :is-shadow="true" shadow="0px 0px 3px 1px rgba(0, 0, 0, 0.08)">
					<text class="uni-body">{{thisSoup.riddle}}</text>
				</uni-card>
			</view>
			<view class="hint">
				<uni-card title="线索" :is-shadow="true" shadow="0px 0px 3px 1px rgba(0, 0, 0, 0.08)">
					<text class="uni-body" v-for="(item, index) in thisSoup.hint" :key="index">{{item}}</text>
				</uni-card>
			</view>
			<view class="answer">
				<uni-card title="汤面" :is-shadow="true" shadow="0px 0px 3px 1px rgba(0, 0, 0, 0.08)">
					<text class="uni-body">{{thisSoup.answer}}</text>
				</uni-card>
			</view>
		</view>
		
		<view class="footer">
			<!-- 这里展示详情收藏评分分享 -->
			<view class="detail">
				<uni-icons type="more" size="30" color="$text-color-1"></uni-icons>
				<view class="text">详情</view>
			</view>
			<view class="love">
				<uni-icons type="heart" size="30" color="$text-color-1"></uni-icons>
				<view class="text">收藏</view>
			</view>
			<view class="rate">
				<uni-icons type="star" size="30" color="$text-color-1"></uni-icons>
				<view class="text">评分</view>
			</view>
			<view class="share">
				<uni-icons type="redo" size="30" color="$text-color-1"></uni-icons>
				<view class="text">分享</view>
			</view>
		</view>
	</view>
</template>

<script setup>
import { onLoad } from '@dcloudio/uni-app'
import {ref} from 'vue'
import soupList from '@/static/soupText/soupInfo.json'
const id = ref(0)
const thisSoup = ref(null)
//拿到当前海龟汤的函数
const getSoupDetail = (id) => {
	thisSoup.value = soupList.find(item => item.id === id)
}
//通过options拿到参数：与浏览器的vue router不一样，这是小程序的原生方法
onLoad((options) => {
	id.value = options.id
	console.log(id.value)
	getSoupDetail(id.value)
	console.log(thisSoup)
})


</script>

<style lang="scss" scoped>
	.soupDetailLayout{
		overflow:hidden;
		.head{
			width:85vw;
			margin:20rpx auto;
			display:flex;
			flex-direction:column;
			justify-content:space-around;
			padding:20rpx 20rpx;
			.avatar{
				display:flex;
				align-items:center;
				image{
					width:140rpx;
					height:140rpx;
					border-radius:80rpx;
				}
				.userInfo{
					padding-left:40rpx;
					display:flex;
					flex-direction:column;
					.userName{
						font-size:40rpx;
						color:$text-color-1;
					}
					.userId{
						font-size:20rpx;
						color:$text-color-2;
					}
				}
			}
			.soupInfo{
				width:100%;
				margin-top:20rpx;
				display:flex;
				align-items:center;
				justify-content:space-evenly;
				.title{
					font-size:30rpx;
					color:$text-color-1;
				}
				.tag{
					font-size:25rpx;
					color:$text-color-1;
				}
			}
		}
		.body{
			.hint{
				.uni-body{
					display:flex;
					flex-direction:column;
				}
			}
		}
.footer {
	position: fixed;
	bottom: 0; // 上移一段距离，避开 tabBar
	left: 0;
	width: 100%;
	height: 100rpx;
	display: flex;
	justify-content: space-around;
	align-items: center;
	background-color: #fff;
	z-index: 999;

	border-top: 1px solid #eee;

	view {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		font-size: 24rpx;
		color: $text-color-1;
	}
}

	}
</style>
