<script setup lang="ts">
import axios from '@/util/axiosInstance';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import { useTokenStore } from '@/stores/token';

const route = useRoute()
const router = useRouter()
const toast = useToast()
const tokenStore = useTokenStore()

const loadding = ref<boolean>(true)
const product = ref()
const quantity = ref<any>(1)
const recommends = ref()

async function add() {
    const res = await axios.post("/shopping_cart/add", {
        product_id: route.params.id,
        quantity: quantity.value,
        token: tokenStore.token
    })
    if (res.data.status === 200) {
        toast.add({ 'severity': 'success', 'summary': '成功', 'detail': '加入购物车成功！', 'life': 3000 })
        await new Promise((resolve) => setTimeout(resolve, 3000))
        router.push("/cart")
    } else {
        toast.add({ 'severity': 'error', 'summary': '失败', 'detail': '账号未登录，请先登录账号。', 'life': 3000 })
    }
}

const goNext = (id: string) => {
    router.push('/product/' + id);
    window.location.replace('#/product/' + id)
    window.location.reload()
}

onMounted(async () => {
    const res = await axios.post("/product/detail", {
        product_id: route.params.id
    })
    if (res.data.status === 200) {
        product.value = res.data.product
    } else {
        return toast.add({ 'severity': 'error', 'summary': '失败', 'detail': '数据加载失败:' + res.data.message, 'life': 3000 })
    }

    const ans = await axios.get("/product/recommend")
    if (ans.data.status === 200) {
        recommends.value = ans.data.products
    } else {
        return toast.add({ 'severity': 'error', 'summary': '失败', 'detail': '数据加载失败:' + res.data.message, 'life': 3000 })
    }
    loadding.value = false
})
</script>

<template>
    <div class="h-full w-full flex flex-col">
        <Toast></Toast>
        <Header></Header>
        <Search></Search>
        <section v-if="!loadding" class="flex justify-center items-center mt-6 mb-2 py-4 w-full">
            <div class="m-2 flex flex-row flex-wrap-reverse gap-8 items-center justify-center gap-5rem">
                <div class="flex justify-center w-full max-w-500px">
                    <Image v-if="product.pictures" :src="product.pictures" :alt="product.comment"
                        image-class="max-w-full" class="max-w-full" preview />
                </div>
                <div class="flex flex-col items-start w-85">
                    <h1>{{ product.name }}</h1>
                    <span class="text-shadow-color-blue">{{ product.detail }}</span>
                    <Divider></Divider>
                    <div class="inline-flex flex-wrap gap-2">
                        <Tag :value="product.category"></Tag>
                    </div>
                    <div class="my-2 flex flex-col gap-3 b-rd bg-gray-300 w-full">
                        <div class="inline-flex accent-coolgray gap-5 items-start px-8 py-2 mt-2">
                            <h3 class="m-0">定价</h3>
                            <span class="text-xl text-red">￥{{ product.price }}</span>
                        </div>
                        <div class="inline-flex accent-coolgray gap-5 items-center px-8 py-2 mb-2">
                            <h3 class="m-0">库存</h3>
                            <span>{{ product.quantity }} 件</span>
                        </div>
                    </div>
                    <div class="flex justify-end w-full py-2 mt-3">
                        <div class="flex flex-col gap-2rem">
                            <InputText v-model="quantity" class="w-full" />
                            <Slider v-model="quantity" class="w-full" :min="1" :max="product.quantity" />
                            <Button @click="add" label="加入购物车"></Button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        <section v-else class="flex flex-col items-center justify-center m-10">
            <ProgressSpinner></ProgressSpinner>
        </section>
        <Divider><i class="pi pi-shopping-cart"></i> 商品规格</Divider>
        <div class="flex w-full justify-center items-center">
            <div class="flex flex-col w-full max-w-600px">
                <div v-if="product" class="flex flex-col items-start w-full">
                    <span v-for="param in product.spec_param" class="text-coolGray">{{ param }}</span>
                </div>
                <div v-else>
                    <span>暂无商品数据</span>
                </div>
            </div>
        </div>
        <Divider><i class="pi pi-heart-fill"></i> 你可能还喜欢</Divider>
        <div class="flex mt-2 p-4 flex-row flex-wrap items-center justify-around justify-start">
            <div v-for="product in recommends" class="m-1 mt-4">
                <Card @click="goNext(product.id)" style="width: 25rem; overflow: hidden">
                    <template #header>
                        <img class="h-96 w-full" alt="user header" :src="product.pictures" />
                    </template>
                    <template #title>{{ product.name }}</template>
                    <template #footer>
                        <div class="text-2xl text-orange">

                            ￥ {{ product.price }}
                        </div>
                    </template>
                </Card>
            </div>
        </div>
        <Footer></Footer>
    </div>
</template>

<style scoped></style>