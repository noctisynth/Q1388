<script setup lang="ts">
import { useTokenStore } from "@/stores/token";
import Button from "primevue/button";
import { ref } from "vue";

const UserToken = useTokenStore();
console.log(UserToken.token);

const recommends = ref([
  {
    id: '1000',
    code: 'f230fh0g3',
    name: 'Bamboo Watch',
    description: 'Product Description',
    image: 'bamboo-watch.jpg',
    price: 65,
    category: 'Accessories',
    quantity: 24,
    inventoryStatus: 'INSTOCK',
    rating: 5
  },
  {
    id: '1000',
    code: 'f230fh0g3',
    name: 'Bamboo Watch',
    description: 'Product Description',
    image: 'bamboo-watch.jpg',
    price: 65,
    category: 'Accessories',
    quantity: 24,
    inventoryStatus: 'INSTOCK',
    rating: 5
  },
]);
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

const products = ref([
  {
    id: '1000',
    code: 'f230fh0g3',
    name: 'Bamboo Watch',
    description: 'Product Description',
    image: 'bamboo-watch.jpg',
    price: 65,
    category: 'Accessories',
    quantity: 24,
    inventoryStatus: 'INSTOCK',
    rating: 5
  },
  {
    id: '1000',
    code: 'f230fh0g3',
    name: 'Bamboo Watch',
    description: 'Product Description',
    image: 'bamboo-watch.jpg',
    price: 65,
    category: 'Accessories',
    quantity: 24,
    inventoryStatus: 'INSTOCK',
    rating: 5
  },
])
</script>

<template>
  <main class="flex flex-col">
    <Header></Header>
    <div class="flex justify-center w-full h-full">
      <div class="flex flex-col w-full max-w-960px gap-6">
        <Carousel :value="recommends" :numVisible="3" :numScroll="3" :responsiveOptions="responsiveOptions" circular
          :autoplayInterval="3000">
          <template #item="slotProps">
            <div class="border-1 surface-border b-rd m-2 p-3">
              <div class="mb-3">
                <div class="relative mx-auto">
                  <img :src="'https://primefaces.org/cdn/primevue/images/product/' + slotProps.data.image"
                    :alt="slotProps.data.name" class="w-full b-rd" />
                  <Tag :value="slotProps.data.inventoryStatus" :severity="'info'" class="absolute"
                    style="left:5px; top: 5px" />
                </div>
              </div>
              <div class="mb-3 font-medium">{{ slotProps.data.name }}</div>
              <div class="flex justify-between items-center">
                <div class="mt-0 font-semibold text-xl">${{ slotProps.data.price }}</div>
                <span>
                  <Button icon="pi pi-heart" severity="secondary" outlined></Button>
                  <Button icon="pi pi-shopping-cart" class="ml-2"></Button>
                </span>
              </div>
            </div>
          </template>
        </Carousel>
        <DataView :value="products" dataKey="id">
          <template #list="slotProps">
            <div class="grid">
              <div v-for="(item, index) in slotProps.items" :key="index">
                <div class="flex flex-col sm:flex-row sm:items-center p-4 gap-3"
                  :class="{ 'b-t-1 surface-border': index !== 0 }">
                  <div class="md:w-10rem relative">
                    <img class="block xl:block mx-auto border-round w-full"
                      :src="`https://primefaces.org/cdn/primevue/images/product/${item.image}`" :alt="item.name" />
                    <Tag :value="item.inventoryStatus" :severity="'info'" class="absolute" style="left: 4px; top: 4px">
                    </Tag>
                  </div>
                  <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-4">
                    <div class="flex flex-row md:flex-col justify-between items-start gap-2">
                      <div>
                        <span class="font-medium text-secondary text-sm">{{ item.category }}</span>
                        <div class="text-lg font-medium text-900 mt-2">{{ item.name }}</div>
                      </div>
                      <div class="surface-100 p-1" style="border-radius: 30px">
                        <div class="surface-0 flex items-center gap-2 justify-center py-1 px-2"
                          style="border-radius: 30px; box-shadow: 0px 1px 2px 0px rgba(0, 0, 0, 0.04), 0px 1px 2px 0px rgba(0, 0, 0, 0.06)">
                          <span class="text-900 font-medium text-sm">{{ item.rating }}</span>
                          <i class="pi pi-star-fill text-yellow-500"></i>
                        </div>
                      </div>
                    </div>
                    <div class="flex flex-col md:items-end gap-5">
                      <span class="text-xl font-semibold text-900">${{ item.price }}</span>
                      <div class="flex flex-row-reverse md:flex-row gap-2">
                        <Button icon="pi pi-heart" outlined></Button>
                        <Button icon="pi pi-shopping-cart" label="Buy Now"
                          :disabled="item.inventoryStatus === 'OUTOFSTOCK'"
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
    </div>
    <Footer></Footer>
  </main>
</template>
