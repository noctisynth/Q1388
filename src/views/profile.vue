<script setup lang="ts">
import axios from "@/util/axiosInstance";

import { md5 } from "js-md5";

import { onMounted, reactive, ref } from "vue";

const items = ref([
    {
        label: '主页',
        icon: 'pi pi-home'
    },
    {
        label: '用户',
        icon: 'pi pi-user',
        items: [
            {
                label: '登录',
                icon: 'pi pi-sign-in'
            },
            {
                label: '注册',
                icon: 'pi pi pi-plus-circle'
            }
        ]
    },
]);

const user = reactive<any>({
    username: null,
    email: null,
    addresses: null,
    default_address: null,
    avatar: null
});



async function initUser() {

    await axios.get("/account/profile").then(res => {
        let data = res.data
        if (data['status'] == 200) {
            user.username = data["username"]
            user.email = data["email"]
            user.addresses = data["addresses"]
            user.default_address = data["default_address"]
            user.avatar = data["avatar"]
        } else {
            // 之后做重定向跳转
            axios.post("/account/login", {
                'username': "bash",
                'password': md5("123456"),
            })
        }
    })

}

const visible = ref(false);
const password = ref("");
const email = ref("");
const default_address = ref("");
const address = ref("");

async function update_user() {
    visible.value = false;
    let data: any = {};
    if (password.value.length != 0) {
        data["password"] = md5(password.value);
    }
    if (email.value.length != 0) {
        data["email"] = email.value;
    }
    if (default_address.value.length != 0) {
        data["default_address"] = default_address.value;
    }
    if (address.value.length != 0) {
        data["addresses"] = [address.value];
    }

    await axios.post("/account/update", data).then(res => {
        if (res.data["status"] == 200) {
            window.location.reload();
        }
    })

}

async function del_address(address: any) {
    await axios.post("/account/del_address", {
        "address": address
    }).then(res => {
        if (res.data["status"] == 200) {
            console.log(res.data)
        }

    });
}
onMounted(() => {
    initUser();
})
</script>

<template>
    <main>
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
        <div class="flex justify-center">
            <div class="w-full max-w-960px">
                <div class="mt-4 flex flex-col">
                    <Avatar :image="user.avatar" class="mb-4" size="xlarge" shape="circle" />

                    <Button class="w-20" label="修改" @click="visible = true" />

                    <Dialog v-model:visible="visible" modal header="Edit Profile" :style="{ width: '25rem' }">
                        <span class="p-text-secondary block mb-5">Update your information.</span>
                        <div class="flex align-items-center gap-3 mb-3">
                            <label for="password" class="font-semibold w-6rem">密码</label>
                            <InputText id="password" class="flex-auto" autocomplete="off" v-model="password" />
                        </div>
                        <div class="flex align-items-center gap-3 mb-5">
                            <label for="email" class="font-semibold w-6rem">邮件</label>
                            <InputText id="email" class="flex-auto" autocomplete="off" v-model="email" />
                        </div>
                        <div class="flex align-items-center gap-3 mb-5">
                            <label for="default_address" class="font-semibold w-6rem">默认地址</label>
                            <InputText id="default_address" class="flex-auto" autocomplete="off"
                                v-model="default_address" />
                        </div>
                        <div class="flex align-items-center gap-3 mb-5">
                            <label for="address" class="font-semibold w-6rem">添加地址</label>
                            <InputText id="address" class="flex-auto" autocomplete="off" v-model="address" />
                        </div>
                        <div class="flex justify-content-end gap-2">
                            <Button type="button" label="Cancel" severity="secondary" @click="visible = false"></Button>
                            <Button type="button" label="Save" @click="update_user()"></Button>
                        </div>
                    </Dialog>

                    <h2>用户名：{{ user.username }}</h2>
                    <p>邮件：{{ user.email }}</p>
                    <p>默认地址：{{ user.default_address }}</p>
                    <p>地址：</p>
                    <li v-for="address in user.addresses">{{ address }}
                        <button @click="del_address(address)">Del</button>
                    </li>
                </div>
            </div>
        </div>
    </main>
</template>
