// API基础URL，指向后端服务器地址
const API_BASE_URL = 'http://127.0.0.1:5000'

// 存储在本地的令牌键名
const TOKEN_KEY = 'auth_token'
// 存储在本地的用户信息键名
const USER_KEY = 'auth_user'

/**
 * 获取本地存储的认证令牌
 * @returns {string|null} 认证令牌或null
 */
function getToken() {
	try {
		return uni.getStorageSync(TOKEN_KEY) || null
	} catch (e) {
		return null
	}
}

/**
 * 保存认证令牌到本地存储
 * @param {string} token - 认证令牌
 */
function setToken(token) {
	try {
		uni.setStorageSync(TOKEN_KEY, token)
	} catch (e) {
		console.error('保存令牌失败:', e)
	}
}

/**
 * 从本地存储移除认证令牌
 */
function removeToken() {
	try {
		uni.removeStorageSync(TOKEN_KEY)
	} catch (e) {
		console.error('移除令牌失败:', e)
	}
}

/**
 * 获取本地存储的用户信息
 * @returns {object|null} 用户信息对象或null
 */
function getUser() {
	try {
		const userStr = uni.getStorageSync(USER_KEY)
		return userStr ? JSON.parse(userStr) : null
	} catch (e) {
		return null
	}
}

/**
 * 保存用户信息到本地存储
 * @param {object} user - 用户信息对象
 */
function setUser(user) {
	try {
		uni.setStorageSync(USER_KEY, JSON.stringify(user))
	} catch (e) {
		console.error('保存用户信息失败:', e)
	}
}

/**
 * 从本地存储移除用户信息
 */
function removeUser() {
	try {
		uni.removeStorageSync(USER_KEY)
	} catch (e) {
		console.error('移除用户信息失败:', e)
	}
}

/**
 * 获取认证请求头
 * @returns {object} 包含Authorization头的对象
 */
function getAuthHeader() {
	const token = getToken()
	return token ? { 'Authorization': `Bearer ${token}` } : {}
}

/**
 * 发送API请求
 * @param {string} url - API接口路径
 * @param {object} options - 请求选项
 * @returns {Promise<any>} 请求结果
 */
async function request(url, options = {}) {
	const fullUrl = `${API_BASE_URL}${url}`
	const header = {
		'Content-Type': 'application/json',
		...getAuthHeader(),
		...options.header
	}
	
	try {
		const response = await uni.request({
			url: fullUrl,
			header: header,
			...options
		})
		
		if (response[1]) {
			const data = response[1]
			if (data.statusCode >= 200 && data.statusCode < 300) {
				return data.data
			} else {
				const error = new Error(data.data?.error || '请求失败')
				error.response = data
				throw error
			}
		}
		
		throw new Error('网络请求失败')
	} catch (error) {
		console.error('请求错误:', error)
		throw error
	}
}

/**
 * 微信手机号一键登录
 * @returns {Promise<any>} 登录结果
 */
async function wechatLogin() {
	try {
		// 调用微信获取手机号API
		const { code } = await uni.login({
			provider: 'weixin'
		});
		
		// 获取用户信息
		const { userInfo } = await uni.getUserProfile({
			desc: '用于完善会员资料'
		});
		
		// 调用后端微信登录接口
		const result = await request('/api/wechat-login', {
			method: 'POST',
			data: {
				code,
				userInfo: userInfo
			}
		});
		
		// 保存登录状态
		if (result.token && result.user) {
			setToken(result.token);
			setUser(result.user);
		}
		
		return result;
	} catch (error) {
		console.error('微信登录失败:', error);
		throw error;
	}
}

/**
 * 获取微信手机号
 * @param {object} e - 微信授权事件对象
 * @returns {Promise<string>} 手机号
 */
async function getWechatPhoneNumber(e) {
	if (e.detail.errMsg !== 'getPhoneNumber:ok') {
		throw new Error('用户拒绝授权获取手机号');
	}
	
	try {
		// 调用后端接口解密手机号
		const result = await request('/api/decrypt-phone', {
			method: 'POST',
			data: {
				encryptedData: e.detail.encryptedData,
				iv: e.detail.iv,
				code: (await uni.login()).code
			}
		});
		
		return result.phoneNumber;
	} catch (error) {
		console.error('获取手机号失败:', error);
		throw error;
	}
}

/**
 * 用户退出登录
 * @returns {Promise<object>} 退出结果
 */
async function logout() {
	try {
		await request('/api/logout', {
			method: 'POST'
		})
	} catch (error) {
		console.log('退出登录API调用失败，继续本地退出流程')
	}
	
	removeToken()
	removeUser()
	
	return { success: true, message: '退出成功' }
}

/**
 * 获取用户信息
 * @returns {Promise<any>} 用户信息
 */
async function getProfile() {
	return await request('/api/profile', {
		method: 'GET'
	})
}

/**
 * 验证令牌有效性
 * @returns {Promise<any>} 验证结果
 */
async function verifyToken() {
	return await request('/api/verify-token', {
		method: 'GET'
	})
}

/**
 * 检查用户是否已登录
 * @returns {boolean} 是否已登录
 */
function isLoggedIn() {
	const token = getToken()
	const user = getUser()
	return !!(token && user)
}

/**
 * 获取当前登录用户信息
 * @returns {object|null} 用户信息
 */
function getCurrentUser() {
	return getUser()
}

/**
 * 检查认证状态
 * @returns {Promise<object>} 认证状态信息
 */
async function checkAuthStatus() {
	const token = getToken()
	
	if (!token) {
		return { isLoggedIn: false }
	}
	
	try {
		const result = await verifyToken()
		
		if (result.valid) {
			const storedUser = getUser()
			if (!storedUser || storedUser.user_id !== result.user.user_id) {
				setUser({
					user_id: result.user.user_id,
					username: result.user.username,
					email: result.user.email
				})
			}
			return {
				isLoggedIn: true,
				user: result.user
			}
		} else {
			removeToken()
			removeUser()
			return { isLoggedIn: false, reason: result.error }
		}
	} catch (error) {
		console.error('认证检查失败:', error)
		return { isLoggedIn: false, reason: '验证失败' }
	}
}

export {
	setToken,
	removeToken,
	setUser,
	removeUser,
	getAuthHeader,
	wechatLogin,
	getWechatPhoneNumber,
	logout,
	getProfile,
	verifyToken,
	isLoggedIn,
	getCurrentUser,
	checkAuthStatus,
	API_BASE_URL
}

export default {
	setToken,
	removeToken,
	setUser,
	removeUser,
	getAuthHeader,
	wechatLogin,
	getWechatPhoneNumber,
	logout,
	getProfile,
	verifyToken,
	isLoggedIn,
	getCurrentUser,
	checkAuthStatus,
	API_BASE_URL
}
