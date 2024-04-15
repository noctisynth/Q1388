<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import { FilterMatchMode } from 'primevue/api';
import Toast from 'primevue/toast';
import { useRouter } from 'vue-router';
import axios from '@/util/axiosInstance';

const router = useRouter()
const toast = useToast()
const products = ref()
const loadding = ref<boolean>(true)
const categories = ref();

const refresh = async () => {
    loadding.value = true
    const res = await axios.get("/product/all")
    if (res.data) {
        products.value = res.data.products
        loadding.value = false
        toast.add({ 'severity': 'success', 'summary': '成功', 'detail': "数据加载成功", 'life': 3000 })
    } else {
        toast.add({ 'severity': 'error', 'summary': '失败', 'detail': "数据加载失败:" + res.data.message, 'life': 3000 })
    }
}

const filters = ref({
    name: { value: null, matchMode: FilterMatchMode.CONTAINS },
    categories: { value: null, matchMode: FilterMatchMode.CONTAINS },
});

onMounted(async () => {
    refresh()
})
</script>

<template>
    <div class="h-full w-full flex flex-col">
        <Toast class="max-w-90%"></Toast>
        <Header></Header>
        <div class="flex justify-center py-3rem max-w-full">
            <DataTable dateKey="id" paginator :rows="10" class="max-w-960px w-full" :value="products"
                :loading="loadding" v-model:filters="filters" filterDisplay="row">
                <template #header>
                    <div class="flex flex-wrap items-center justify-between gap-2">
                        <span class="text-xl text-900 font-bold">产品</span>
                        <Button @click="refresh" icon="pi pi-refresh" rounded raised></Button>
                    </div>
                </template>
                <Column field="name" header="名称" :showFilterMenu="false">
                    <template #body="slotProps">
                        <div class="flex items-start flex-col gap-2">
                            <div>
                                <h2 class="m-0 text-size-sm">{{ slotProps.data.name }}</h2>
                            </div>
                            <span class="text-coolGray text-xs">{{ slotProps.data.spec_param }}</span>
                        </div>
                    </template>
                    <template #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" type="text" @input="filterCallback()"
                            class="p-column-filter min-w-5rem" placeholder="搜索" />
                    </template>
                </Column>
                <Column header="图片">
                    <template #body="slotProps">
                        <div class="flex justify-center items-center flex-col gap-2">
                            <img :src="slotProps.data.pictures" :alt="slotProps.data.name" class="w-6rem b-rd" />
                            <span class="text-coolGray text-xs">{{ slotProps.data.comment }}</span>
                        </div>
                    </template>
                </Column>
                <Column field="price" header="价格" sortable>
                    <template #body="slotProps">
                        ￥{{ slotProps.data.price }}
                    </template>
                </Column>
                <Column field="quantity" header="余量" sortable></Column>
                <Column field="categories" header="分类" :showFilterMenu="false">
                    <template #body="slotProps">
                        <Tag v-for="category in slotProps.data.categories" :value="category"></Tag>
                    </template>
                    <template #filter="{ filterModel, filterCallback }">
                        <MultiSelect v-model="filterModel.value" @change="filterCallback()" :options="categories"
                            placeholder="选择" class="p-column-filter">
                            <template #option="slotProps">
                                <div class="flex items-center">
                                    <Tag :value="slotProps.option"></Tag>
                                </div>
                            </template>
                        </MultiSelect>
                    </template>
                </Column>
                <Column class="!p-0 !m-0">
                    <template #body="{ data }">
                        <Button @click="router.push('/product/' + data.id)" icon="pi pi-send" plain outlined></Button>
                    </template>
                </Column>
                <template #footer> 共 {{ products ? products.length : 0 }} 个产品 </template>
            </DataTable>
        </div>
        <Footer></Footer>
    </div>
</template>

<style scoped></style>