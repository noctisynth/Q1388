<script setup lang="ts">
import { ref } from 'vue';

const product = ref({
    "id": 1,
    "name": "手机",
    "price": 1000,
    "quantity": 10,
    "spec_param": "4G手机",
    "categories": [
        "电子产品"
    ],
    "comment": "很好用的手机",
    "detail": "这是一个很好用的手机",
    "pictures": "https://primefaces.org/cdn/primevue/images/galleria/galleria10.jpg"
})

const recommends = ref([
    {
        "id": 1,
        "name": "手机",
        "price": 1000,
        "quantity": 10,
        "spec_param": "4G手机",
        "categories": [
            "电子产品"
        ],
        "comment": "很好用的手机",
        "detail": "这是一个很好用的手机",
        "pictures": "https://primefaces.org/cdn/primevue/images/galleria/galleria10.jpg"
    },
    {
        "id": 2,
        "name": "T恤",
        "price": 20,
        "quantity": 50,
        "spec_param": "纯棉T恤",
        "categories": [
            "服装"
        ],
        "comment": "舒适的T恤",
        "detail": "这是一件舒适的T恤",
        "pictures": "https://primefaces.org/cdn/primevue/images/galleria/galleria10.jpg"
    },
    {
        "id": 3,
        "name": "Python编程入门",
        "price": 50,
        "quantity": 30,
        "spec_param": "Python编程入门书籍",
        "categories": [
            "图书"
        ],
        "comment": "学习编程的好书",
        "detail": "这是一本Python编程入门的好书",
        "pictures": "https://primefaces.org/cdn/primevue/images/galleria/galleria10.jpg"
    }
])
</script>

<template>
    <div class="h-full w-full flex flex-col">
        <Header></Header>
        <section class="flex justify-center items-center mt-6 mb-2 py-4 w-full">
            <div class="m-2 flex flex-row flex-wrap-reverse gap-8 items-center justify-center">
                <div class="flex justify-center w-full max-w-300px">
                    <Image :src="product.pictures" :alt="product.comment" image-class="max-w-full" class="max-w-full"
                        preview />
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
                    <div class="flex justify-between w-full py-2 mt-3">
                        <Button severity="secondary" label="加入购物车"></Button>
                        <Button label="立即下单"></Button>
                    </div>
                </div>
            </div>
        </section>
        <Divider><i class="pi pi-heart-fill"></i> 你可能还喜欢</Divider>
        <div class="flex justify-center items-center mt-6 mb-2 py-4 w-full">
            <DataView :value="recommends" dataKey="id">
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