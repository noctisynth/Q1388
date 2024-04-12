<script setup lang="ts">
import { ref } from "vue";

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
</script>

<template>
  <main>
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
    <div class="flex justify-center">
      <div class="w-full max-w-960px">
        <Carousel :value="products" :numVisible="3" :numScroll="3" :responsiveOptions="responsiveOptions" circular :autoplayInterval="3000">
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
      </div>
    </div>
  </main>
</template>
