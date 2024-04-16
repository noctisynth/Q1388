<script setup lang="ts">
import axios from '@/util/axiosInstance';
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import { useTokenStore } from '@/stores/token';
import { useRoute, useRouter } from 'vue-router';
import Toast from 'primevue/toast';

const router = useRouter()
const route = useRoute()

const active = ref<number>(0)
if (route.query.register)
    active.value = 1

const username = ref<string | null>()
const password = ref<string | null>()
const password_confirm = ref<string | null>()
const email = ref<string | null>()
const tokenStore = useTokenStore()
const toast = useToast()
if (tokenStore.isLoggedIn())
    router.push("/")

async function login() {
    const res = await axios.post("/account/login", {
        username: username.value,
        password: password.value,
        token: 123,
    })
    if (res.data.status === 200) {
        tokenStore.setToken(res.data.token)
        toast.add({
            'severity': 'success', 'summary': '成功', 'detail': '登录成功！', 'life': 3000
        })
        await new Promise((resolve) => setTimeout(resolve, 3000))
        router.push("/")
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
    const res = await axios.post("/account/add", {
        username: username.value,
        password: password.value,
        email: email.value
    })
    if (res.data.status === 200) {
        toast.add({
            'severity': 'success', 'summary': '成功', 'detail': res.data.message, 'life': 3000
        })
        router.push("/login");
        await new Promise((resolve) => setTimeout(resolve, 3000))
        router.go(0)
    } else {
        toast.add({
            'severity': 'error', 'summary': '失败', 'detail': res.data.message, 'life': 3000
        })
        await new Promise((resolve) => setTimeout(resolve, 3000))
    }
}
</script>

<template>
    <div class="w-full h-full flex flex-col bg-gray-200">
        <Toast></Toast>
        <Header></Header>
        <div class="flex justify-center items-center my-2rem mx-1.5rem gap-3rem py-2rem">
            <section class="max-w-2xl w-600px">
                <Card class="w-full">
                    <template #content>
                        <TabView v-model:activeIndex="active">
                            <TabPanel header="登录">
                                <div class="flex gap-3 items-center justify-center flex-col w-full p-5">
                                    <span class="p-text-secondary">请输入你的账号密码</span>
                                    <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                                        <label for="username" class="font-semibold">用户名</label>
                                        <InputText v-model="username" id="username" class="w-full" />
                                    </div>
                                    <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                                        <label for="password" class="font-semibold">密码</label>
                                        <Password v-model="password" inputId="password" inputClass="w-full"
                                            class="w-full" />
                                    </div>
                                </div>
                                <div class="flex justify-end gap-2">
                                    <Button @click="login" type="button" label="登录"></Button>
                                </div>
                            </TabPanel>
                            <TabPanel header="注册">
                                <div class="flex gap-3 items-center justify-center flex-col w-full p-5">
                                    <span class="p-text-secondary">注册一个新的账户</span>
                                    <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                                        <label for="register-username" class="font-semibold">用户名</label>
                                        <InputText v-model="username" id="register-username" class="w-full" />
                                    </div>
                                    <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                                        <label for="email" class="font-semibold">邮箱</label>
                                        <InputText v-model="email" id="email" class="w-full" />
                                    </div>
                                    <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                                        <label for="register-password" class="font-semibold">密码</label>
                                        <Password v-model="password" inputId="register-password" inputClass="w-full"
                                            class="w-full" />
                                    </div>
                                    <div class="flex flex-col w-full max-w-70% px-1rem gap-1rem">
                                        <label for="password-confirm" class="font-semibold">密码确认</label>
                                        <Password v-model="password_confirm" inputId="password-confirm"
                                            inputClass="w-full" class="w-full" />
                                    </div>
                                </div>
                                <div class="flex justify-end gap-2">
                                    <Button @click="register" type="button" label="注册"></Button>
                                </div>
                            </TabPanel>
                        </TabView>
                    </template>
                </Card>
            </section>
        </div>
        <Footer></Footer>
    </div>
</template>

<style scoped></style>