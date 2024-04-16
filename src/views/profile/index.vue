<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useTokenStore } from "@/stores/token";
import { md5 } from "js-md5";
import { useToast } from "primevue/usetoast";
import Toast from "primevue/toast";
import router from "@/router";
import axios from "@/util/axiosInstance";

const toast = useToast();

const user = reactive<any>({
    username: null,
    email: null,
    addresses: null,
    default_address: null,
    avatar: null
});


const tokenStore = useTokenStore();

async function initUser() {
    if (!tokenStore.isLoggedIn()) {
        toast.add({ severity: 'error', summary: '错误', detail: '用户未登录！', life: 3000 });
        await new Promise((resolve) => setTimeout(resolve, 3000))
        return router.push("/")
    }
    const res = await axios.post("/account/profile", { "token": tokenStore.token })
    let data = res.data
    if (data.status == 200) {
        user.username = data["username"]
        user.email = data["email"]
        user.addresses = data["addresses"]
        user.default_address = data["default_address"]
        user.avatar = data["avatar"]
    } else {
        toast.add({ severity: 'error', summary: '错误', detail: '登录密钥已过期，请重新登录！', life: 3000 });
        await new Promise((resolve) => setTimeout(resolve, 3000))
        tokenStore.removeToken()
        router.push("/")
    }
}

const visible = ref(false);
const checkout_visible = ref(false);
const password = ref("");
const email = ref("");
const default_address = ref("");
const address = ref("");

async function update_user() {
    visible.value = false;
    let data: any = {};
    data["token"] = tokenStore.token
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
        if (res.data.status == 200) {
            toast.add({ severity: 'success', summary: '资料', detail: '用户资料修改成功', life: 3000 });
            router.go(0)
        }
    })

}

async function del_address(address: any) {
    const res = await axios.post("/account/del_address", {
        "address": address,
        "token": tokenStore.token
    })
    console.log(res.data);
    toast.add({ severity: 'success', summary: '地址', detail: '地址删除成功', life: 3000 });
    await new Promise((resolve) => setTimeout(resolve, 3000))
    router.go(0)
}

const orders = ref<any>([])
async function get_products() {
    await axios.post("/order/all", {
        "token": tokenStore.token
    }).then(res => {
        console.log(res.data)
        if (res.status == 200) {
            let data = res.data;
            orders.value = data.orders;
        }
    })
}
async function cancel_order(order_id: any) {
    await axios.post("/order/cancel", {
        "order_id": order_id,
        "token": tokenStore.token
    }).then(res => {
        let data = res.data;
        if (data.status == 200) {
            router.go(0)
        }
    })
}
onMounted(async () => {
    await initUser();
    await get_products();
})
const value = ref('货到付款');
const options = ref(['货到付款', '在线支付']);
async function checkout(order_id: any) {
    checkout_visible.value = false
    if (value.value == '在线支付') {

    }
    await axios.post("/order/pay", {
        "order_id": order_id,
        "token": tokenStore.token
    }).then(res => {
        let data = res.data;
        if (data.status == 200) {

            toast.add({ severity: 'success', summary: '支付', detail: '支付成功', life: 6000 });
            router.go(0)

        }
        console.log(data)
    })
}


const address_visible = ref(false)
async function modify_address(order_id: any) {
    await axios.post("/order/modify_address", {
        "order_id": order_id,
        "address": address.value,
        "token": tokenStore.token
    }).then(res => {
        let data = res.data;
        if (data.status == 200) {
            toast.add({ severity: 'success', summary: '修改地址', detail: '修改成功', life: 3000 });
            router.go(0)
        }
    })
}
const expandedRows = ref({});
</script>

<template>
    <div class="flex flex-col">
        <Toast class="max-w-90%"></Toast>
        <Header></Header>

        <div class="flex justify-center w-full h-full">
            <div class="flex flex-col w-full  gap-6">
                <div class="mt-4 flex flex-col items-center">
                    <Avatar :image="user.avatar" class="mb-4" size="xlarge" shape="circle" />
                    <Button class="w-20" label="修改" @click="visible = true"></Button>
                    <Dialog v-model:visible="visible" modal header="编辑信息" :style="{ width: '25rem' }">
                        <span class="p-text-secondary block mb-5">更新你的个人信息</span>
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
                    <h2>{{ user.username }}</h2>
                    <div class="flex-col justify-start">
                        <p>邮件：{{ user.email }}</p>
                        <p>默认地址：{{ user.default_address }}</p>
                        <p>地址：</p>
                        <li class="mt-2" v-for="address in user.addresses">{{ address }}
                            <Button type="button" label="删除" @click="del_address(address)"></Button>
                        </li>
                    </div>
                </div>

                <DataTable v-model:expandedRows="expandedRows" :value="orders" dataKey="id"
                    tableStyle="min-width: 100rem">
                    <Column expander style="width: 1rem" />
                    <Column field="id" header="订单ID"></Column>
                    <Column field="total_price" header="订单价格"></Column>
                    <Column field="status" header="顶单状态"></Column>
                    <Column field="date" header="下单日期"></Column>
                    <Column field="address" header="收货地址"></Column>
                    <Column header="操作">
                        <template #body="slotProps">
                            <Button @click="checkout_visible = true" label="支付"></Button>
                            <Button @click="cancel_order(slotProps.data.id)" label="取消" class="ml-2"></Button>
                            <Button @click="address_visible = true" label=" 修改地址" class="ml-2"></Button>
                            <Dialog v-model:visible="checkout_visible" modal header="支付订单" :style="{ width: '25rem' }">
                                <span class="p-text-secondary block mb-5">请选择支付方式</span>
                                <SelectButton v-model="value" :options="options" aria-labelledby="basic" />
                                <div class="mt-4" v-if="value == '在线支付'"><svg viewBox="0 0 49 49" width="100%"
                                        height="100%" fill="#ffffff" xmlns="http://www.w3.org/2000/svg">
                                        <rect fill="#ffffff" width="100%" height="100%"></rect>
                                        <path
                                            d="M0 0v1h7v-1zM12 0v1h1v-1zM16 0v1h2v-1zM20 0v1h3v-1zM25 0v1h2v-1zM28 0v1h1v-1zM35 0v1h1v-1zM37 0v1h1v-1zM40 0v1h1v-1zM42 0v1h7v-1zM0 1v1h1v-1zM6 1v1h1v-1zM9 1v1h2v-1zM13 1v1h1v-1zM20 1v1h2v-1zM23 1v1h4v-1zM34 1v1h2v-1zM37 1v1h4v-1zM42 1v1h1v-1zM48 1v1h1v-1zM0 2v1h1v-1zM2 2v1h3v-1zM6 2v1h1v-1zM9 2v1h1v-1zM11 2v1h3v-1zM15 2v1h1v-1zM18 2v1h3v-1zM22 2v1h1v-1zM25 2v1h3v-1zM29 2v1h1v-1zM31 2v1h4v-1zM36 2v1h2v-1zM39 2v1h2v-1zM42 2v1h1v-1zM44 2v1h3v-1zM48 2v1h1v-1zM0 3v1h1v-1zM2 3v1h3v-1zM6 3v1h1v-1zM9 3v1h3v-1zM13 3v1h1v-1zM17 3v1h3v-1zM23 3v1h1v-1zM26 3v1h1v-1zM28 3v1h3v-1zM32 3v1h1v-1zM34 3v1h4v-1zM39 3v1h1v-1zM42 3v1h1v-1zM44 3v1h3v-1zM48 3v1h1v-1zM0 4v1h1v-1zM2 4v1h3v-1zM6 4v1h1v-1zM8 4v1h2v-1zM12 4v1h2v-1zM16 4v1h2v-1zM20 4v1h7v-1zM29 4v1h1v-1zM31 4v1h3v-1zM35 4v1h3v-1zM42 4v1h1v-1zM44 4v1h3v-1zM48 4v1h1v-1zM0 5v1h1v-1zM6 5v1h1v-1zM12 5v1h2v-1zM15 5v1h1v-1zM17 5v1h1v-1zM20 5v1h3v-1zM26 5v1h3v-1zM32 5v1h1v-1zM38 5v1h1v-1zM42 5v1h1v-1zM48 5v1h1v-1zM0 6v1h7v-1zM8 6v1h1v-1zM10 6v1h1v-1zM12 6v1h1v-1zM14 6v1h1v-1zM16 6v1h1v-1zM18 6v1h1v-1zM20 6v1h1v-1zM22 6v1h1v-1zM24 6v1h1v-1zM26 6v1h1v-1zM28 6v1h1v-1zM30 6v1h1v-1zM32 6v1h1v-1zM34 6v1h1v-1zM36 6v1h1v-1zM38 6v1h1v-1zM40 6v1h1v-1zM42 6v1h7v-1zM8 7v1h1v-1zM15 7v1h3v-1zM19 7v1h2v-1zM22 7v1h1v-1zM26 7v1h1v-1zM28 7v1h1v-1zM30 7v1h1v-1zM32 7v1h1v-1zM37 7v1h1v-1zM39 7v1h2v-1zM2 8v1h2v-1zM6 8v1h4v-1zM12 8v1h1v-1zM15 8v1h4v-1zM22 8v1h7v-1zM30 8v1h1v-1zM32 8v1h2v-1zM37 8v1h1v-1zM41 8v1h2v-1zM44 8v1h1v-1zM1 9v1h1v-1zM3 9v1h3v-1zM8 9v1h1v-1zM10 9v1h3v-1zM14 9v1h2v-1zM18 9v1h1v-1zM20 9v1h4v-1zM27 9v1h2v-1zM31 9v1h1v-1zM35 9v1h2v-1zM42 9v1h4v-1zM0 10v1h1v-1zM3 10v1h1v-1zM5 10v1h4v-1zM11 10v1h4v-1zM16 10v1h1v-1zM18 10v1h4v-1zM23 10v1h1v-1zM27 10v1h1v-1zM29 10v1h2v-1zM34 10v1h2v-1zM39 10v1h5v-1zM45 10v1h2v-1zM1 11v1h1v-1zM4 11v1h1v-1zM7 11v1h1v-1zM9 11v1h2v-1zM13 11v1h2v-1zM17 11v1h1v-1zM22 11v1h5v-1zM29 11v1h1v-1zM34 11v1h2v-1zM37 11v1h1v-1zM39 11v1h1v-1zM41 11v1h7v-1zM2 12v1h1v-1zM5 12v1h3v-1zM9 12v1h9v-1zM20 12v1h1v-1zM24 12v1h3v-1zM30 12v1h3v-1zM34 12v1h3v-1zM38 12v1h4v-1zM43 12v1h1v-1zM46 12v1h1v-1zM0 13v1h1v-1zM2 13v1h1v-1zM4 13v1h2v-1zM7 13v1h1v-1zM10 13v1h1v-1zM15 13v1h1v-1zM18 13v1h1v-1zM24 13v1h1v-1zM26 13v1h4v-1zM31 13v1h3v-1zM35 13v1h1v-1zM37 13v1h2v-1zM43 13v1h2v-1zM47 13v1h2v-1zM0 14v1h1v-1zM3 14v1h1v-1zM6 14v1h1v-1zM8 14v1h1v-1zM10 14v1h1v-1zM13 14v1h1v-1zM15 14v1h1v-1zM19 14v1h1v-1zM21 14v1h2v-1zM25 14v1h1v-1zM28 14v1h1v-1zM38 14v1h1v-1zM41 14v1h3v-1zM45 14v1h3v-1zM1 15v1h2v-1zM7 15v1h1v-1zM9 15v1h1v-1zM11 15v1h2v-1zM14 15v1h1v-1zM16 15v1h2v-1zM19 15v1h4v-1zM26 15v1h3v-1zM30 15v1h1v-1zM34 15v1h2v-1zM37 15v1h4v-1zM42 15v1h3v-1zM48 15v1h1v-1zM0 16v1h3v-1zM5 16v1h9v-1zM15 16v1h1v-1zM17 16v1h1v-1zM20 16v1h4v-1zM26 16v1h3v-1zM30 16v1h1v-1zM32 16v1h1v-1zM34 16v1h1v-1zM39 16v1h1v-1zM43 16v1h2v-1zM46 16v1h1v-1zM0 17v1h6v-1zM7 17v1h6v-1zM16 17v1h1v-1zM18 17v1h4v-1zM23 17v1h1v-1zM28 17v1h1v-1zM30 17v1h1v-1zM32 17v1h2v-1zM35 17v1h1v-1zM38 17v1h1v-1zM40 17v1h1v-1zM48 17v1h1v-1zM3 18v1h1v-1zM5 18v1h2v-1zM8 18v1h1v-1zM10 18v1h1v-1zM12 18v1h1v-1zM14 18v1h4v-1zM23 18v1h3v-1zM29 18v1h1v-1zM32 18v1h2v-1zM35 18v1h2v-1zM41 18v1h3v-1zM45 18v1h1v-1zM48 18v1h1v-1zM0 19v1h2v-1zM8 19v1h1v-1zM10 19v1h1v-1zM15 19v1h4v-1zM22 19v1h1v-1zM25 19v1h1v-1zM27 19v1h3v-1zM32 19v1h1v-1zM36 19v1h2v-1zM41 19v1h1v-1zM43 19v1h1v-1zM45 19v1h1v-1zM2 20v1h3v-1zM6 20v1h2v-1zM12 20v1h1v-1zM14 20v1h1v-1zM17 20v1h1v-1zM19 20v1h1v-1zM24 20v1h1v-1zM32 20v1h2v-1zM35 20v1h1v-1zM38 20v1h2v-1zM45 20v1h1v-1zM47 20v1h1v-1zM0 21v1h1v-1zM5 21v1h1v-1zM7 21v1h3v-1zM11 21v1h3v-1zM17 21v1h1v-1zM19 21v1h1v-1zM24 21v1h2v-1zM29 21v1h1v-1zM31 21v1h1v-1zM35 21v1h2v-1zM39 21v1h1v-1zM41 21v1h2v-1zM46 21v1h1v-1zM0 22v1h1v-1zM2 22v1h9v-1zM17 22v1h3v-1zM21 22v1h6v-1zM32 22v1h1v-1zM34 22v1h1v-1zM36 22v1h1v-1zM39 22v1h6v-1zM46 22v1h1v-1zM0 23v1h1v-1zM4 23v1h1v-1zM8 23v1h3v-1zM13 23v1h1v-1zM15 23v1h1v-1zM17 23v1h1v-1zM21 23v1h2v-1zM26 23v1h4v-1zM33 23v1h1v-1zM36 23v1h1v-1zM38 23v1h1v-1zM40 23v1h1v-1zM44 23v1h3v-1zM1 24v1h4v-1zM6 24v1h1v-1zM8 24v1h1v-1zM10 24v1h1v-1zM12 24v1h4v-1zM17 24v1h3v-1zM21 24v1h2v-1zM24 24v1h1v-1zM26 24v1h1v-1zM28 24v1h1v-1zM34 24v1h3v-1zM40 24v1h1v-1zM42 24v1h1v-1zM44 24v1h1v-1zM46 24v1h1v-1zM0 25v1h2v-1zM4 25v1h1v-1zM8 25v1h2v-1zM16 25v1h1v-1zM19 25v1h1v-1zM21 25v1h2v-1zM26 25v1h4v-1zM31 25v1h3v-1zM35 25v1h6v-1zM44 25v1h2v-1zM47 25v1h1v-1zM1 26v1h1v-1zM4 26v1h5v-1zM10 26v1h1v-1zM12 26v1h3v-1zM17 26v1h2v-1zM20 26v1h1v-1zM22 26v1h6v-1zM31 26v1h1v-1zM35 26v1h2v-1zM38 26v1h1v-1zM40 26v1h8v-1zM1 27v1h2v-1zM5 27v1h1v-1zM9 27v1h3v-1zM13 27v1h1v-1zM18 27v1h3v-1zM23 27v1h2v-1zM27 27v1h1v-1zM31 27v1h2v-1zM35 27v1h1v-1zM37 27v1h1v-1zM40 27v1h2v-1zM43 27v1h1v-1zM48 27v1h1v-1zM0 28v1h1v-1zM4 28v1h4v-1zM9 28v1h2v-1zM13 28v1h1v-1zM15 28v1h9v-1zM26 28v1h8v-1zM37 28v1h1v-1zM44 28v1h4v-1zM1 29v1h1v-1zM3 29v1h3v-1zM7 29v1h3v-1zM11 29v1h5v-1zM20 29v1h1v-1zM22 29v1h1v-1zM24 29v1h2v-1zM27 29v1h3v-1zM33 29v1h3v-1zM44 29v1h2v-1zM47 29v1h2v-1zM0 30v1h1v-1zM3 30v1h4v-1zM8 30v1h2v-1zM11 30v1h1v-1zM13 30v1h2v-1zM17 30v1h1v-1zM19 30v1h3v-1zM24 30v1h2v-1zM28 30v1h1v-1zM30 30v1h1v-1zM33 30v1h2v-1zM36 30v1h7v-1zM44 30v1h5v-1zM1 31v1h1v-1zM5 31v1h1v-1zM7 31v1h3v-1zM11 31v1h2v-1zM14 31v1h1v-1zM16 31v1h6v-1zM29 31v1h1v-1zM32 31v1h1v-1zM34 31v1h2v-1zM37 31v1h1v-1zM39 31v1h1v-1zM41 31v1h3v-1zM5 32v1h2v-1zM8 32v1h1v-1zM11 32v1h5v-1zM17 32v1h2v-1zM21 32v1h2v-1zM24 32v1h2v-1zM27 32v1h1v-1zM29 32v1h1v-1zM32 32v1h5v-1zM38 32v1h1v-1zM40 32v1h1v-1zM42 32v1h1v-1zM44 32v1h2v-1zM47 32v1h1v-1zM0 33v1h2v-1zM5 33v1h1v-1zM11 33v1h1v-1zM14 33v1h2v-1zM18 33v1h3v-1zM26 33v1h5v-1zM32 33v1h1v-1zM37 33v1h1v-1zM39 33v1h4v-1zM45 33v1h1v-1zM1 34v1h1v-1zM5 34v1h2v-1zM8 34v1h2v-1zM15 34v1h2v-1zM18 34v1h2v-1zM25 34v1h1v-1zM30 34v1h2v-1zM34 34v1h1v-1zM36 34v1h1v-1zM39 34v1h1v-1zM43 34v1h1v-1zM45 34v1h2v-1zM1 35v1h2v-1zM5 35v1h1v-1zM8 35v1h4v-1zM14 35v1h2v-1zM20 35v1h3v-1zM25 35v1h2v-1zM28 35v1h3v-1zM32 35v1h1v-1zM35 35v1h3v-1zM39 35v1h1v-1zM42 35v1h1v-1zM44 35v1h1v-1zM46 35v1h1v-1zM3 36v1h1v-1zM6 36v1h2v-1zM9 36v1h1v-1zM12 36v1h2v-1zM15 36v1h5v-1zM26 36v1h1v-1zM28 36v1h2v-1zM31 36v1h1v-1zM33 36v1h1v-1zM35 36v1h2v-1zM39 36v1h3v-1zM44 36v1h3v-1zM0 37v1h1v-1zM3 37v1h3v-1zM7 37v1h1v-1zM9 37v1h5v-1zM15 37v1h1v-1zM18 37v1h1v-1zM22 37v1h1v-1zM24 37v1h2v-1zM27 37v1h1v-1zM30 37v1h1v-1zM33 37v1h1v-1zM35 37v1h1v-1zM38 37v1h3v-1zM42 37v1h1v-1zM44 37v1h2v-1zM47 37v1h2v-1zM1 38v1h1v-1zM5 38v1h4v-1zM11 38v1h4v-1zM16 38v1h1v-1zM21 38v1h3v-1zM26 38v1h3v-1zM31 38v1h1v-1zM33 38v1h1v-1zM38 38v1h2v-1zM41 38v1h1v-1zM43 38v1h2v-1zM47 38v1h1v-1zM1 39v1h3v-1zM7 39v1h3v-1zM11 39v1h1v-1zM13 39v1h6v-1zM21 39v1h1v-1zM23 39v1h2v-1zM26 39v1h1v-1zM32 39v1h2v-1zM35 39v1h1v-1zM44 39v1h2v-1zM47 39v1h1v-1zM0 40v1h3v-1zM6 40v1h4v-1zM13 40v1h1v-1zM15 40v1h1v-1zM17 40v1h2v-1zM20 40v1h1v-1zM22 40v1h5v-1zM28 40v1h6v-1zM37 40v1h2v-1zM40 40v1h5v-1zM48 40v1h1v-1zM8 41v1h1v-1zM11 41v1h1v-1zM13 41v1h1v-1zM15 41v1h1v-1zM18 41v1h2v-1zM21 41v1h2v-1zM26 41v1h1v-1zM28 41v1h1v-1zM30 41v1h3v-1zM34 41v1h1v-1zM36 41v1h2v-1zM39 41v1h2v-1zM44 41v1h3v-1zM48 41v1h1v-1zM0 42v1h7v-1zM8 42v1h1v-1zM11 42v1h1v-1zM13 42v1h3v-1zM17 42v1h1v-1zM19 42v1h1v-1zM22 42v1h1v-1zM24 42v1h1v-1zM26 42v1h3v-1zM31 42v1h2v-1zM36 42v1h2v-1zM40 42v1h1v-1zM42 42v1h1v-1zM44 42v1h2v-1zM47 42v1h2v-1zM0 43v1h1v-1zM6 43v1h1v-1zM12 43v1h4v-1zM17 43v1h1v-1zM19 43v1h2v-1zM22 43v1h1v-1zM26 43v1h2v-1zM30 43v1h2v-1zM33 43v1h2v-1zM36 43v1h2v-1zM40 43v1h1v-1zM44 43v1h2v-1zM47 43v1h1v-1zM0 44v1h1v-1zM2 44v1h3v-1zM6 44v1h1v-1zM10 44v1h1v-1zM15 44v1h2v-1zM19 44v1h1v-1zM21 44v1h7v-1zM33 44v1h1v-1zM38 44v1h1v-1zM40 44v1h6v-1zM47 44v1h1v-1zM0 45v1h1v-1zM2 45v1h3v-1zM6 45v1h1v-1zM8 45v1h2v-1zM11 45v1h2v-1zM20 45v1h1v-1zM22 45v1h2v-1zM30 45v1h2v-1zM36 45v1h2v-1zM39 45v1h1v-1zM41 45v1h2v-1zM44 45v1h1v-1zM48 45v1h1v-1zM0 46v1h1v-1zM2 46v1h3v-1zM6 46v1h1v-1zM8 46v1h1v-1zM10 46v1h5v-1zM19 46v1h1v-1zM21 46v1h1v-1zM24 46v1h1v-1zM26 46v1h1v-1zM28 46v1h3v-1zM34 46v1h4v-1zM39 46v1h3v-1zM43 46v1h4v-1zM0 47v1h1v-1zM6 47v1h1v-1zM9 47v1h1v-1zM11 47v1h1v-1zM13 47v1h2v-1zM17 47v1h1v-1zM19 47v1h2v-1zM27 47v1h1v-1zM29 47v1h5v-1zM36 47v1h2v-1zM43 47v1h1v-1zM45 47v1h2v-1zM0 48v1h7v-1zM11 48v1h1v-1zM15 48v1h3v-1zM25 48v1h2v-1zM29 48v1h1v-1zM36 48v1h3v-1zM40 48v1h2v-1zM43 48v1h1v-1zM45 48v1h4v-1z"
                                            fill="#000000"></path>
                                    </svg>
                                </div>
                                <div class="mt-2 flex justify-content-end gap-2">
                                    <Button type="button" label="支付" @click="checkout(slotProps.data.id)"></Button>
                                </div>
                            </Dialog>
                            <Dialog v-model:visible="address_visible" modal header="修改地址" :style="{ width: '25rem' }">
                                <div class="flex align-items-center gap-3 mb-5">
                                    <label for="address" class="font-semibold w-6rem">修改地址</label>
                                    <InputText id="address" class="flex-auto" autocomplete="off" v-model="address" />
                                </div>
                                <div class="mt-2 flex justify-content-end gap-2">
                                    <Button type="button" label="修改"
                                        @click="modify_address(slotProps.data.id)"></Button>
                                </div>
                            </Dialog>
                        </template>
                    </Column>

                    <template #expansion="slotProps">

                        <DataTable :value="slotProps.data.order_items">
                            <Column field="product.name" header="商品名称"></Column>
                            <Column class="ml-2" header="图片">
                                <template #body="slotProps">
                                    <Image v-if="slotProps.data.product.pictures" :src="slotProps.data.product.pictures"
                                        :alt="slotProps.data.product.comment" image-class="w-6rem b-rd"
                                        class="w-6rem b-rd" preview />
                                </template>
                            </Column>
                            <Column field="product.price" header="商品价格" sortable></Column>
                            <Column field="quantity" header="购买数量" sortable></Column>
                            <Column field="price" header="小计" sortable>
                            </Column>
                        </DataTable>

                    </template>
                </DataTable>










            </div>
        </div>

        <Footer></Footer>
    </div>
</template>
