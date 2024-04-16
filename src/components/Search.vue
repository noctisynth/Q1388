<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { ref } from 'vue'

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
</script>

<template>
    <div class="flex items-center justify-center w-full my-3rem px-2rem gap-3rem">
        <img alt="Django Shop" src="/favicon.png" class="w-20"></img>
        <div class="max-w-800px w-full flex flex-row gap-1rem">
            <InputText v-model="input" @keypress.enter="search" class="w-full" placeholder="搜索商品"></InputText>
            <Button @click="search" icon="pi pi-search"></Button>
        </div>
    </div>
</template>

<style scoped></style>
