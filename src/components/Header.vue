<script setup lang="ts">
import { useTokenStore } from '@/stores/token';
import axios from '@/util/axiosInstance';
import Password from 'primevue/password';
import { useToast } from 'primevue/usetoast';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const emit = defineEmits(['onSearch'])
const router = useRouter()
const route = useRoute()
const tokenStore = useTokenStore()
const toast = useToast()
const showRegister = ref<boolean>(false)
const input = ref()


let user_items;
if (!tokenStore.isLoggedIn())
    user_items = [
        {
            label: '登录',
            icon: 'pi pi-sign-in',
            command: () => {
                router.push('/login')
            }
        },
        {
            label: '注册',
            icon: 'pi pi pi-plus-circle',
            command: () => {
                router.push('/login?register=1')
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

const search = () => {
    if (route.path !== '/product' && route.path !== '/product/')
        router.push('/product?key=' + input.value)
    emit('onSearch', input.value)
}
</script>

<template>
    <Menubar :model="items" class="!border-x-none !b-rd-0" breakpoint="600px">
        <template #start>
            <img alt="Django Shop" src="/favicon.png" class="w-10"></img>
        </template>
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
                <InputText @keypress.enter="search" v-model="input" placeholder="搜索" type="text"
                    class="w-8rem sm:w-auto" />
            </div>
        </template>
    </Menubar>
</template>

<style scoped></style>