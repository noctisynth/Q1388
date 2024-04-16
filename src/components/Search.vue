<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue'
import axios from '@/util/axiosInstance';

const route = useRoute()
const router = useRouter()

const emit = defineEmits(['onSearch'])

const input = ref()
if (route.query.key) {
    input.value = route.query.key
    if (route.path.startsWith('/product'))
        emit('onSearch', input.value)
}
else
    input.value = ""

const search = () => {
    if (route.path !== '/product' && route.path !== '/product/')
        router.push('/product?key=' + input.value)
    emit('onSearch', input.value)
}

const into_categories = (category: any) => {
    router.push('/product?category=' + category)
    emit('onSearch', category)
}

const categories = ref<any>([]);
function getRandomElements(array: any, numElements: any) {
    var newArray = array.slice();
    var result = [];
    for (var i = 0; i < numElements; i++) {
        var randomIndex = Math.floor(Math.random() * newArray.length);
        result.push(newArray[randomIndex]);
        newArray.splice(randomIndex, 1);
    }
    return result;
}
onMounted(() => {
    axios.get("/product/categories").then(res => {
        let data = res.data;
        let a = getRandomElements(data.categories, 5);
        categories.value = a;
    })
})
</script>

<template>
    <div class="flex items-center justify-center w-full my-3rem px-2rem gap-3rem">
        <img alt="Django Shop" src="/favicon.png" class="w-20"></img>
        <div class="flex-col max-w-800px w-full flex">
            <div class="max-w-800px w-full flex flex-row gap-1rem">
                <InputText v-model="input" @keypress.enter="search" class="w-full" placeholder="搜索商品"></InputText>
                <Button @click="search" icon="pi pi-search"></Button>
            </div>
            <div class="flex flex-row justify-start mt-3 gap-2rem max-w-auto">
                <!-- <Button v-for="category in categories" :label="category" severity="secondary" rounded /> -->
                <Button plain text v-for="category in categories" @click="into_categories(category)">{{ category
                    }}</Button>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
