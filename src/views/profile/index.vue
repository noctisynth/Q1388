<script setup lang="ts">
import { useTokenStore } from "@/stores/token";
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


const UserToken = useTokenStore();
UserToken.setToken("!xPucFegOlcGcKHSJefV0kuvuetiTokZ6qtpQozhA");


async function initUser() {

    await axios.post("/account/profile", { "token": UserToken.token }).then(res => {
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
    data["token"] = UserToken.token
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
        "address": address,
        "token": UserToken.token
    }).then(res => {
        console.log(res.data);
        window.location.reload();
    });
}

const orders = ref<any>([])
async function get_products() {
    await axios.post("/order/all", {
        "token": UserToken.token
    }).then(res => {
        console.log(res.data)
        if (res.status == 200) {
            let data = res.data;
            orders.value = data.orders;

        }
    })
}
onMounted(() => {
    initUser();
    get_products();
})
</script>

<template>
    <div>
        <Header></Header>

        <div class="flex justify-center">
            <div class="w-full max-w-960px flex flex-row">
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
                <div class="ml-96 mt-10">
                    <div v-for="order in orders">
                        <span>订单id: {{ order.id }}</span>
                        <div>订单状态: {{ order.status }}</div>
                        <div>下单日期: {{ order.date }}</div>
                        <div>收货地址: {{ orders.address }}</div>
                        <div>支付价格: {{ order.total_price }}</div>
                        <span>商品：</span>
                        <div class="mt-4" v-for="item in order.order_items">
                            <div>名称: {{ item.product.name }}</div>
                            <div>数量: {{ item.product.quantity }}</div>
                        </div>
                    </div>

                </div>

            </div>
        </div>

        <Footer></Footer>
    </div>
</template>
