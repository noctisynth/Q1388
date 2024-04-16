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
        if (data.status === 200) {
            router.push("/profile")
        } else {
            alert("结算错误")
        }
    })
}

onMounted(() => {
    initCartData()
})
const selectedItem = ref<any[]>([]);
const selectAll = ref(false);

// Function to handle select all checkbox
const onSelectAllChange = (event: any) => {
    selectAll.value = event.checked;
    selectedItem.value = selectAll.value ? [...cart_items.value] : [];
    calculateTotalPrice();
};

// Function to handle individual row selection
const onRowSelect = (event: any) => {
    calculateTotalPrice()
};

// Function to calculate total price of selected items
const calculateTotalPrice = () => {
    total_price.value = selectedItem.value.reduce((total, item) => total + item.price, 0);
};

</script>
<template>
    <main class="flex flex-col">
        <Toast class="max-w-90%"></Toast>
        <Header></Header>
        <div class="flex justify-center w-full h-full">

            <div class="m-4">
                <DataTable :value="cart_items" tableStyle="min-width: 80rem" v-model:selection="selectedItem"
                    :selectAll="selectAll" @select-all-change="onSelectAllChange" @rowSelect="onRowSelect"
                    @row-unselect="onRowSelect">

                    <template #header>
                        <div class="flex flex-wrap align-items-center justify-between gap-2">
                            <span class="text-xl text-900 font-bold">购物车</span>
                            <span>总价格：{{ total_price }}</span> <!-- 显示总价格 -->
                            <Button @click="checkout()" label="结算"></Button>
                        </div>
                    </template>
                    <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                    <Column field="product.name" header="名称"></Column>
                    <Column header="图片">
                        <template #body="slotProps">
                            <Image v-if="slotProps.data.product.pictures" :src="slotProps.data.product.pictures"
                                :alt="slotProps.data.product.comment" image-class="w-6rem b-rd" class="w-6rem b-rd"
                                preview />

                        </template>
                    </Column>
                    <Column field="price" header="总价格"></Column>
                    <Column field="product.price" header="单价"></Column>
                    <Column field="quantity" header="数量"></Column>
                    <Column header="数量变更">
                        <template #body="slotProps">
                            <Button @click="add_product(slotProps.data.product.id)" label="+"></Button>
                            <Button @click="del_product(slotProps.data.product.id)" label="-" class="ml-2"></Button>
                        </template>
                    </Column>

                </DataTable>
            </div>
        </div>
        <Footer></Footer>
    </main>
</template>
