<template>
	<view class="search-page pageBg">
		<!-- 顶部搜索栏 -->
		<view class="search-bar">
			<view class="search-input-wrap">
				<uni-icons type="search" size="20" color="#7d7d7d"></uni-icons>
				<input
					class="search-input"
					type="text"
					v-model="keyword"
					placeholder="输入关键词搜索海龟汤（标题 / 汤面 / 标签）"
					confirm-type="search"
					@confirm="handleSearch"
					@input="handleInput"
				/>
				<uni-icons
					v-if="keyword"
					type="clear"
					size="18"
					color="#ccc"
					@click="clearKeyword"
				></uni-icons>
			</view>
			<view class="cancel-btn" @click="goBack">取消</view>
		</view>

		<!-- 搜索建议 or 结果统计 -->
		<view class="search-info">
			<text v-if="!keyword">试试搜索：入门 / 惊悚 / 情感 / 职场</text>
			<text v-else>找到 {{ filteredList.length }} 条相关海龟汤</text>
		</view>

		<!-- 结果列表 -->
		<scroll-view scroll-y class="result-list">
			<view
				class="result-item"
				v-for="item in filteredList"
				:key="item.id"
			>
				<uni-card
					@click="goToDetail(item.id)"
					:title="item.title"
					:extra="item.tag"
					:is-shadow="true"
					shadow="0px 0px 3px 1px rgba(0, 0, 0, 0.08)"
				>
					<text class="riddle-text">{{ item.riddle }}</text>
				</uni-card>
			</view>

			<view v-if="keyword && filteredList.length === 0" class="empty">
				<text>没有找到相关的海龟汤，换个关键词试试吧～</text>
			</view>
		</scroll-view>
	</view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import soupList from '@/static/soupText/soupInfo.json'

const keyword = ref('')

// 过滤逻辑：在标题、汤面、标签中模糊匹配
const filteredList = computed(() => {
	const k = keyword.value.trim().toLowerCase()
	if (!k) return soupList

	return soupList.filter(item => {
		const title = (item.title || '').toLowerCase()
		const riddle = (item.riddle || '').toLowerCase()
		const tag = (item.tag || '').toLowerCase()
		return (
			title.includes(k) ||
			riddle.includes(k) ||
			tag.includes(k)
		)
	})
})

const handleSearch = () => {
	// 此处逻辑交给 computed 即可，保留函数用于回车搜索
}

const handleInput = () => {
	// 实时搜索，交给 computed 处理即可
}

const clearKeyword = () => {
	keyword.value = ''
}

const goBack = () => {
	uni.navigateBack()
}

// 如果后面需要支持从发现页带默认关键字，可在 onLoad 中接收参数
onMounted(() => {
	// TODO: 预留入口，如从 discover 传入 ?q=xxx
})

const goToDetail = (id) => {
	uni.navigateTo({
		url: '/pages/soupDetail/soupDetail?id=' + id
	})
}
</script>

<style lang="scss" scoped>
.search-page {
	display: flex;
	flex-direction: column;
	height: 100vh;
	padding: 20rpx 24rpx 40rpx;
	box-sizing: border-box;
}

.search-bar {
	display: flex;
	align-items: center;
	margin-top: 10rpx;
	margin-bottom: 20rpx;
}

.search-input-wrap {
	flex: 1;
	height: 72rpx;
	border-radius: 36rpx;
	background: rgba(255, 255, 255, 0.95);
	display: flex;
	align-items: center;
	padding: 0 24rpx;
	box-sizing: border-box;
	box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);

	:deep() {
		.uni-icons {
			margin-right: 10rpx;
		}
	}
}

.search-input {
	flex: 1;
	height: 100%;
	font-size: 28rpx;
	color: #333;
}

.cancel-btn {
	margin-left: 20rpx;
	font-size: 28rpx;
	color: #666;
}

.search-info {
	font-size: 24rpx;
	color: #888;
	margin-bottom: 10rpx;
	padding: 0 4rpx;
}

.result-list {
	flex: 1;
	margin-top: 10rpx;
}

.result-item {
	padding-bottom: 10rpx;

	:deep() {
		.uni-card {
			margin-bottom: 16rpx;
			border-radius: 20rpx;
			background: rgba(255, 255, 255, 0.96);
			box-shadow: 0 6rpx 18rpx rgba(0, 0, 0, 0.06);
		}
	}
}

.riddle-text {
	font-size: 28rpx;
	color: #666;
	line-height: 1.6;
}

.empty {
	margin-top: 80rpx;
	text-align: center;
	color: #999;
	font-size: 26rpx;
}
</style>
