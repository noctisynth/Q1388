<script setup lang="ts">
import { useTokenStore } from "@/stores/token";
import Button from "primevue/button";
import { ref } from "vue";

const UserToken = useTokenStore();
console.log(UserToken.token);

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
                  <img :src="slotProps.data.pictures" :alt="slotProps.data.name" class="w-full b-rd" />
                  <Tag :value="slotProps.data.categories[0]" severity="info" class="absolute"
                    style="left:5px; top: 5px" />
                </div>
              </div>
              <div class="mb-3 font-medium">{{ slotProps.data.name }}</div>
              <div class="flex justify-between items-center">
                <div class="mt-0 font-semibold text-xl">${{ slotProps.data.price }}</div>
                <span>
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
    </div>
    <Footer></Footer>
  </main>
</template>
