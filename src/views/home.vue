<script setup lang="ts">
import axios from "@/util/axiosInstance";
import Button from "primevue/button";
import Toast from "primevue/toast";
import { useToast } from "primevue/usetoast";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

const loadding = ref<boolean>(true)
const router = useRouter()
const toast = useToast()
const recommends = ref();
const products = ref()
const responsiveOptions = ref([
  {
    breakpoint: '1400px',
    numVisible: 2,
    numScroll: 1
  },
  {
    breakpoint: '767px',
    numVisible: 2,
    numScroll: 1
  },
  {
    breakpoint: '575px',
    numVisible: 1,
    numScroll: 1
  }
]);

onMounted(async () => {
  const res = await axios.get("/product/recommend")
  if (res.data) {

    recommends.value = res.data.products
    loadding.value = false
  } else {
    toast.add({ 'severity': 'error', 'summary': '失败', 'detail': "数据加载失败:" + res.data.message, 'life': 3000 })
  }
  const d = await axios.get("/product/all")
  if (d.data) {
    products.value = d.data.products
  } else {
    toast.add({ 'severity': 'error', 'summary': '失败', 'detail': "数据加载失败:" + res.data.message, 'life': 3000 })
  }
})
</script>

<template>
  <main class="flex flex-col">
    <Toast class="max-w-90%"></Toast>
    <Header></Header>
    <Search></Search>
    <div class="flex justify-center w-full h-full flex-col items-center">
      <div class="flex flex-col w-full max-w-960px gap-6" v-if="!loadding">
        <Carousel :value="recommends" :numVisible="3" :numScroll="3" :responsiveOptions="responsiveOptions" circular
          :autoplayInterval="3000">
          <template #item="slotProps">
            <div class="border-1 surface-border b-rd m-2 p-3">
              <div class="mb-3">
                <div class="relative mx-auto">
                  <img :src="slotProps.data.pictures" :alt="slotProps.data.name" class="w-full b-rd" />
                  <Tag :value="slotProps.data.category" severity="info" class="absolute" style="left:5px; top: 5px" />
                </div>
              </div>
              <div class="mb-3 font-medium">{{ slotProps.data.name }}</div>
              <div class="flex justify-between items-center">
                <div class="mt-0 font-semibold text-xl">${{ slotProps.data.price }}</div>
                <span>
                  <Button @click="router.push('/product/' + slotProps.data.id)" icon="pi pi-shopping-cart"
                    class="ml-2"></Button>
                </span>
              </div>
            </div>
          </template>
        </Carousel>
      </div>
      <div class="flex justify-center items-center" v-else>
        <ProgressSpinner></ProgressSpinner>
      </div>
      <div class="flex mt-2 p-4 flex-row flex-wrap items-center justify-around justify-start">

        <div v-for="product in products" class="m-1 mt-4">
          <Card @click="router.push('/product/' + product.id)" style="width: 25rem; overflow: hidden">
            <template #header>
              <img class="h-96 w-full" :alt="product.name" :src="product.pictures" />
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
    </div>
    <Footer></Footer>
  </main>
</template>
