<script setup lang="ts">
import { useTokenStore } from '@/stores/token';
import axios from '@/util/axiosInstance';
import { md5 } from 'js-md5';
import Password from 'primevue/password';
import { useToast } from 'primevue/usetoast';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const tokenStore = useTokenStore()
const toast = useToast()
const showLogin = ref<boolean>(false)
const showRegister = ref<boolean>(false)
const username = ref<string | null>()
const email = ref<string | null>()
const password = ref<string | null>()
const password_confirm = ref<string | null>()

let user_items;
if (!tokenStore.isLoggedIn())
    user_items = [
        {
            label: '登录',
            icon: 'pi pi-sign-in',
            command: () => {
                showLogin.value = true
                showRegister.value = false
            }
        },
        {
            label: '注册',
            icon: 'pi pi pi-plus-circle',
            command: () => {
                showRegister.value = true
                showLogin.value = false
            }
        }
    ]
else
    user_items = [
        {
            label: '个人中心',
            icon: 'pi pi-user',
            command: () => {
                router.push("/profile")
            }
        },
        {
            label: '购物车',
            icon: 'pi pi-shopping-cart',
            command: () => {
                router.push("/cart")
            }
        },
        {
            label: '退出登录',
            icon: 'pi pi-sign-out',
            command: () => {
                tokenStore.removeToken()
                router.go(0)
            }
        },
    ]

const items = ref([
    {
        label: '主页',
        icon: 'pi pi-home',
        command: () => {
            router.push("/")
        }
    },
    {
        label: '用户',
        icon: 'pi pi-user',
        items: user_items
    },
    {
        label: '产品',
        icon: 'pi pi-box',
        command: () => {
            router.push("/product")
        }
    }
]);

async function login() {
    const passwd = password.value;
    if (!passwd) return
    const res = await axios.post("/account/login", {
        username: username.value,
        password: md5(passwd),
        token: 123,
    })
    if (res.data.status === 200) {
        tokenStore.setToken(res.data.token)
        toast.add({
            'severity': 'success', 'summary': '成功', 'detail': '登录成功！', 'life': 3000
        })
        await new Promise((resolve) => setTimeout(resolve, 3000))
        router.go(0);
        showLogin.value = false
    } else {
        console.log(res.data)
        toast.add({
            'severity': 'error', 'summary': '失败', 'detail': "登录失败: 账号或密码错误！", 'life': 3000
        })
        await new Promise((resolve) => setTimeout(resolve, 3000))
    }
}

async function register() {
    if (password.value !== password_confirm.value) {
        return toast.add({
            'severity': 'error', 'summary': '失败', 'detail': "两次输入的密码不一致", 'life': 3000
        })
    }
    const passwd = password.value;
    if (!passwd) return
    const res = await axios.post("/account/add", {
        username: username.value,
        password: md5(passwd),
        email: email.value
    })
    if (res.data.status === 200) {
        toast.add({
            'severity': 'success', 'summary': '成功', 'detail': res.data.message, 'life': 3000
        })
        await new Promise((resolve) => setTimeout(resolve, 3000))
        showRegister.value = false
        router.go(0);
    } else {
        toast.add({
            'severity': 'error', 'summary': '失败', 'detail': res.data.message, 'life': 3000
        })
        await new Promise((resolve) => setTimeout(resolve, 3000))
    }
}
</script>

<template>
    <Dialog v-model:visible="showLogin" modal header="登录" class="max-w-90% w-xl">
        <span class="p-text-secondary">请输入你的账号密码</span>
        <div class="flex gap-3 items-center justify-center flex-col w-full p-5">
            <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                <label for="username" class="font-semibold">用户名</label>
                <InputText v-model="username" id="username" class="w-full" />
            </div>
            <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                <label for="password" class="font-semibold">密码</label>
                <Password v-model="password" inputId="password" inputClass="w-full" class="w-full" />
            </div>
        </div>
        <div class="flex justify-end gap-2">
            <Button type="button" label="取消" severity="secondary" @click="showLogin = false"></Button>
            <Button @click="login" type="button" label="登录"></Button>
        </div>
    </Dialog>
    <Dialog v-model:visible="showRegister" modal header="注册" class="max-w-90% w-xl">
        <span class="p-text-secondary">注册一个新的账户</span>
        <div class="flex gap-3 items-center justify-center flex-col w-full p-5">
            <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                <label for="username" class="font-semibold">用户名</label>
                <InputText v-model="username" id="username" class="w-full" />
            </div>
            <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                <label for="email" class="font-semibold">邮箱</label>
                <InputText v-model="email" id="email" class="w-full" />
            </div>
            <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                <label for="password" class="font-semibold">密码</label>
                <Password v-model="password" inputId="password" inputClass="w-full" class="w-full" />
            </div>
            <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                <label for="password-confirm" class="font-semibold">密码确认</label>
                <Password v-model="password_confirm" inputId="password-confirm" inputClass="w-full" class="w-full" />
            </div>
        </div>
        <div class="flex justify-end gap-2">
            <Button type="button" label="取消" severity="secondary" @click="showRegister = false"></Button>
            <Button @click="register" type="button" label="注册"></Button>
        </div>
    </Dialog>
    <Menubar :model="items" class="!border-x-none !b-rd-0" breakpoint="600px">
        <template #item="{ item, props, hasSubmenu, root }">
            <a v-ripple class="flex align-items-center" v-bind="props.action">
                <span :class="item.icon"></span>
                <span class="ml-2">{{ item.label }}</span>
                <Badge v-if="item.badge" :class="{ 'ml-auto': !root, 'ml-2': root }" :value="item.badge" />
                <span v-if="item.shortcut"
                    class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{
                        item.shortcut }}</span>
                <i v-if="hasSubmenu"
                    :class="['pi pi-angle-down', { 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root }]"></i>
            </a>
        </template>
        <template #end>
            <div class="flex align-items-center gap-2">
                <InputText placeholder="Search" type="text" class="w-8rem sm:w-auto" />
            </div>
        </template>
    </Menubar>
</template>

<style scoped></style>