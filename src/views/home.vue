<script setup lang="ts">
import Button from "primevue/button";
import { ref } from "vue";

const light = ref<boolean>(!window.matchMedia('(prefers-color-scheme: dark)'));
console.log(light.value)

const items = ref([
  {
    label: '主页',
    icon: 'pi pi-home'
  },
  {
    label: '用户',
    icon: 'pi pi-user',
    items: [
      {
        label: '登录',
        icon: 'pi pi-sign-in'
      },
      {
        label: '注册',
        icon: 'pi pi pi-plus-circle'
      }
    ]
  },
]);

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

const layout = ref<'grid' | 'list'>('grid');
const options = ref(['list', 'grid']);
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
    <Menubar :model="items" class="!border-x-none !b-rd-0" breakpoint="600px">
      <template #item="{ item, props, hasSubmenu, root }">
        <a v-ripple class="flex align-items-center" v-bind="props.action">
          <span :class="item.icon"></span>
          <span class="ml-2">{{ item.label }}</span>
          <Badge v-if="item.badge" :class="{ 'ml-auto': !root, 'ml-2': root }" :value="item.badge" />
          <span v-if="item.shortcut" class="ml-auto border-1 surface-border border-round surface-100 text-xs p-1">{{
            item.shortcut }}</span>
          <i v-if="hasSubmenu"
            :class="['pi pi-angle-down', { 'pi-angle-down ml-2': root, 'pi-angle-right ml-auto': !root }]"></i>
        </a>
      </template>
      <template #end>
        <div class="flex align-items-center gap-2">
          <InputText placeholder="Search" type="text" class="w-8rem sm:w-auto" />
        </div>
      </template>
    </Menubar>
    <div class="flex justify-center w-full h-full">
      <div class="flex flex-col w-full max-w-960px gap-6">
        <Carousel :value="recommends" :numVisible="3" :numScroll="3" :responsiveOptions="responsiveOptions" circular
          :autoplayInterval="3000">
          <template #item="slotProps">
            <div class="border-1 surface-border border-round m-2 p-3">
              <div class="mb-3">
                <div class="relative mx-auto">
                  <img :src="'https://primefaces.org/cdn/primevue/images/product/' + slotProps.data.image"
                    :alt="slotProps.data.name" class="w-full border-round" />
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
                <div class="flex flex-col sm:flex-row sm:align-items-center p-4 gap-3"
                  :class="{ 'border-top-1 surface-border': index !== 0 }">
                  <div class="md:w-10rem relative">
                    <img class="block xl:block mx-auto border-round w-full"
                      :src="`https://primefaces.org/cdn/primevue/images/product/${item.image}`" :alt="item.name" />
                    <Tag :value="item.inventoryStatus" :severity="'info'" class="absolute" style="left: 4px; top: 4px">
                    </Tag>
                  </div>
                  <div class="flex flex-col md:flex-row justify-between md:align-items-center flex-1 gap-4">
                    <div class="flex flex-row md:flex-col justify-between align-items-start gap-2">
                      <div>
                        <span class="font-medium text-secondary text-sm">{{ item.category }}</span>
                        <div class="text-lg font-medium text-900 mt-2">{{ item.name }}</div>
                      </div>
                      <div class="surface-100 p-1" style="border-radius: 30px">
                        <div class="surface-0 flex align-items-center gap-2 justify-content-center py-1 px-2"
                          style="border-radius: 30px; box-shadow: 0px 1px 2px 0px rgba(0, 0, 0, 0.04), 0px 1px 2px 0px rgba(0, 0, 0, 0.06)">
                          <span class="text-900 font-medium text-sm">{{ item.rating }}</span>
                          <i class="pi pi-star-fill text-yellow-500"></i>
                        </div>
                      </div>
                    </div>
                    <div class="flex flex-col md:align-items-end gap-5">
                      <span class="text-xl font-semibold text-900">${{ item.price }}</span>
                      <div class="flex flex-row-reverse md:flex-row gap-2">
                        <Button icon="pi pi-heart" outlined></Button>
                        <Button icon="pi pi-shopping-cart" label="Buy Now"
                          :disabled="item.inventoryStatus === 'OUTOFSTOCK'"
                          class="flex-auto md:flex-initial white-space-nowrap"></Button>
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
    <div :class="[(light ? '!bg-gray-100' : ''), 'flex w-full flex-col justify-center items-center mt-3rem pt-2rem']"
      style="background-color: var(--p-menubar-background);">
      <div class="w-full flex flex-row justify-end px-3">
        <Button icon="pi pi-discord" plain text></Button>
        <Button icon="pi pi-youtube" plain text></Button>
        <Button icon="pi pi-github" plain text></Button>
      </div>
      <Divider></Divider>
      <div class="flex justify-center pb-3rem pt-2rem">
        <span class="text-sm">Copyright 2011-PRESENT © Noctisynth, org.</span>
      </div>
    </div>
  </main>
</template>
