<script>
	import { wechatLogin, isLoggedIn } from './utils/auth.js'
	export default {
		onLaunch: function() {
			console.log('App Launch')
			// 尝试自动登录
			this.autoLogin()
		},
		onShow: function() {
			console.log('App Show')
			// 页面显示时检查登录状态
			this.checkLoginStatus()
		},
		onHide: function() {
			console.log('App Hide')
		},
		methods: {
			// 自动登录
			async autoLogin() {
				try {
					if (!isLoggedIn()) {
						// 尝试静默登录
						await wechatLogin()
						console.log('自动登录成功')
					}
				} catch (error) {
					// 静默登录失败，不提示用户，让用户手动点击登录
					console.log('自动登录失败:', error)
				}
			},
			// 检查登录状态
			checkLoginStatus() {
				if (isLoggedIn()) {
					console.log('用户已登录')
				} else {
					console.log('用户未登录')
				}
			}
		}
	}
</script>

<style>
	/*每个页面公共css */
@import "common/style/common-style.scss"
</style>
