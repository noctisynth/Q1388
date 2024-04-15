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
  const res = await axios.get("/product/all")
  if (res.data) {
    products.value = res.data.products
    recommends.value = res.data.products
    loadding.value = false
  } else {
    toast.add({ 'severity': 'error', 'summary': '失败', 'detail': "数据加载失败:" + res.data.message, 'life': 3000 })
  }
})
</script>

<template>
  <main class="flex flex-col">
    <Toast class="max-w-90%"></Toast>
    <Header></Header>
    <div class="flex justify-center w-full h-full">
      <div class="flex flex-col w-full max-w-960px gap-6" v-if="!loadding">
        <Carousel :value="recommends" :numVisible="3" :numScroll="3" :responsiveOptions="responsiveOptions" circular
          :autoplayInterval="3000">
          <template #item="slotProps">
            <div class="border-1 surface-border b-rd m-2 p-3">
              <div class="mb-3">
                <div class="relative mx-auto">
                  <img :src="slotProps.data.pictures" :alt="slotProps.data.name" class="w-full b-rd" />
                  <Tag :value="slotProps.data.categories[0]" severity="info" class="absolute"
                    style="left:5px; top: 5px" />
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
        <DataView :value="products" dataKey="id">
          <template #empty>
            <div class="flex items-center justify-center">暂无数据。</div>
          </template>
          <template #list="slotProps">
            <div class="grid">
              <div v-for="(item, index) in slotProps.items" :key="index">
                <div class="flex flex-col sm:flex-row sm:items-center p-4 gap-3"
                  :class="{ 'b-t-1 surface-border': index !== 0 }">
                  <div class="md:w-10rem relative">
                    <img class="block xl:block mx-auto b-rd w-full" :src="item.pictures" :alt="item.name" />
                    <Tag :value="item.categories[0]" severity="info" class="absolute" style="left: 4px; top: 4px">
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
                        <Button icon="pi pi-shopping-cart" label="购买" @click="router.push('/product/' + item.id)"
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
      <div class="flex justify-center items-center" v-else>
        <ProgressSpinner></ProgressSpinner>
      </div>
    </div>
    <Footer></Footer>
  </main>
</template>
