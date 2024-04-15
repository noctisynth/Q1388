<script setup lang="ts">
import { useTokenStore } from '@/stores/token';
import axios from '@/util/axiosInstance';
import { onMounted, ref } from 'vue';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const UserToken = useTokenStore();
const router = useRouter()
const cart_items = ref<any[]>([]);
const total_price = ref(0);

async function initCartData() {
    await axios.post("/shopping_cart/all", {
        "token": UserToken.token
    }).then(res => {
        let data = res.data;
        if (res.data.status == 200) {
            cart_items.value = data.cart_items.map((item: any) => ({
                ...item,
                selected: false // 添加选中状态的属性，默认为false
            }));
            total_price.value = data.total_price;
        }
    })
}

async function add_product(product_id: any) {
    console.log(product_id)
    await axios.post("/shopping_cart/add", {
        "product_id": product_id,
        "quantity": 1,
        "token": UserToken.token
    }).then(res => {
        let data = res.data;
        if (data.status === 200) {
            router.go(0)
        }
    })

}
async function del_product(product_id: any) {
    await axios.post("/shopping_cart/del", {
        "product_id": product_id,
        "number": 1,
        "token": UserToken.token
    }).then(res => {
        let data = res.data;
        console.log(data)
        if (data.status === 200) {
            router.go(0)
        }
    })
}
async function checkout() {
    await axios.post("/order/checkout", {
        "token": UserToken.token
    }).then(res => {
        let data = res.data
        console.log(data)
        if (data.status === 200) {
            router.push("/profile")
        } else {
            alert("结算错误")
        }
    })
}

// 计算选中商品的总价格
const select_price = computed(() => {
    return cart_items.value.reduce((total, item) => {
        if (item.selected) {
            return total + item.price;
        }
        return total;
    }, 0);
});

onMounted(() => {
    initCartData()
})

</script>
<template>
    <div class="flex justify-center">

        <div class="mt-4 flex flex-col">
            <button @click="checkout()">结算</button>
            <span>总价格: {{ total_price }}</span>
            <span>选中商品总价格: {{ select_price }}</span>
            <div class="mt-4">
                <div class="mt-10" v-for="item in cart_items" :key="item.id">
                    <div>名称：{{ item.product.name }}</div>
                    <div>商品单价：{{ item.product.price }}</div>
                    <div>数量：{{ item.quantity }}</div>
                    <div>价格：{{ item.price }}
                        <span><button @click="add_product(item.product.id)">+</button></span>
                        <span><button @click="del_product(item.product.id)">-</button></span>
                    </div>
                    <input type="checkbox" v-model="item.selected"> 选中
                </div>
            </div>
        </div>

    </div>
</template>


<style scoped></style>
