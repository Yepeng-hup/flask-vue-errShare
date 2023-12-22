import { ref } from 'vue';

// test 函数
export const myFunc=(num)=>{
    const s = ref(num + 1);
    return s.value;
}