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
        toast.add({ 'severity': 'error', 'summary': '失败', 'detail': '数据加载失败:' + res.data.message, 'life': 3000 })
    }
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

    const ans = await axios.get("/product/all")
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
        <section v-if="!loadding" class="flex justify-center items-center mt-6 mb-2 py-4 w-full">
            <div class="m-2 flex flex-row flex-wrap-reverse gap-8 items-center justify-center">
                <div class="flex justify-center w-full max-w-300px">
                    <Image v-if="product.pictures" :src="product.pictures" :alt="product.comment"
                        image-class="max-w-full" class="max-w-full" preview />
                </div>
                <div class="flex flex-col items-start w-85">
                    <h1>{{ product.name }}</h1>
                    <span class="text-shadow-color-blue">{{ product.detail }}</span>
                    <Divider></Divider>
                    <div class="inline-flex flex-wrap gap-2">
                        <Tag v-for="category in product.categories" :value="`#${category}`"></Tag>
                    </div>
                    <div class="my-2 flex flex-col gap-3 bg-dark w-full">
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
        <Divider><i class="pi pi-heart-fill"></i> 你可能还喜欢</Divider>
        <div class="flex justify-center items-center mt-6 mb-2 py-4 w-full">
            <DataView :value="recommends" dataKey="id">
                <template #empty>
                    <div>暂无数据。</div>
                </template>
                <template #list="slotProps">
                    <div class="grid">
                        <div v-for="(item, index) in slotProps.items" :key="index">
                            <div class="flex flex-col sm:flex-row sm:items-center p-4 gap-3"
                                :class="{ 'b-t-1 surface-border': index !== 0 }">
                                <div class="md:w-10rem relative">
                                    <img class="block xl:block mx-auto b-rd w-full" :src="item.pictures"
                                        :alt="item.name" />
                                    <Tag :value="item.categories[0]" severity="info" class="absolute"
                                        style="left: 4px; top: 4px">
                                    </Tag>
                                </div>
                                <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-4">
                                    <div class="flex flex-row md:flex-col justify-between items-start gap-2">
                                        <div>
                                            <div class="text-lg font-medium text-900 mt-2">{{ item.name }}</div>
                                            <div class="text-sm mt-2 text-coolGray">{{ item.detail }}</div>
                                        </div>
                                        <div></div>
                                    </div>
                                    <div class="flex flex-col md:items-end gap-5">
                                        <span class="text-xl font-semibold text-900">${{ item.price }}</span>
                                        <div class="flex flex-row w-full justify-end">
                                            <Button icon="pi pi-shopping-cart" label="购买"
                                                class="flex-auto md:flex-initial whitespace-nowrap"></Button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </DataView>
        </div>
        <Footer></Footer>
    </div>
</template>

<style scoped></style>