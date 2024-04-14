<script setup lang="ts">
import { useTokenStore } from '@/stores/token';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()
const tokenStore = useTokenStore()
const showLogin = ref<boolean>(false)

let user_items;
if (!tokenStore.isLoggedIn())
    user_items = [
        {
            label: '登录',
            icon: 'pi pi-sign-in',
            command: () => {
                showLogin.value = true
            }
        },
        {
            label: '注册',
            icon: 'pi pi pi-plus-circle',
            command: () => {
                showLogin.value = true
            }
        }
    ]
else
    user_items = [
        {
            label: '个人中心',
            icon: 'pi user',
            command: () => {
                router.push("/profile")
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
</script>

<template>
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