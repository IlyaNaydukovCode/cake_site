// services/mockData.js
export const mockData = {
    // Моковые пользователи
    users: [
      {
        id: 1,
        email: 'test@example.com',
        full_name: 'Иван Иванов',
        phone: '+7 (999) 123-45-67',
        address: 'ул. Примерная, д. 1, кв. 1',
        created_at: '2024-01-15T10:00:00Z'
      }
    ],
  
    // Готовые торты
    cakes: [
      {
        id: 1,
        name: 'Шоколадный торт',
        description: 'Нежный шоколадный торт с кремом из белого шоколада',
        price: 2500,
        weight: 1500,
        image_url: 'https://via.placeholder.com/300x200?text=Шоколадный+торт',
        ingredients: 'Шоколад, мука, яйца, сливки, сахар'
      },
      {
        id: 2,
        name: 'Клубничный торт',
        description: 'Воздушный бисквит со свежей клубникой',
        price: 2800,
        weight: 1400,
        image_url: 'https://via.placeholder.com/300x200?text=Клубничный+торт',
        ingredients: 'Клубника, бисквит, сливки, сахар'
      },
      {
        id: 3,
        name: 'Медовик',
        description: 'Классический медовый торт со сметанным кремом',
        price: 2200,
        weight: 1600,
        image_url: 'https://via.placeholder.com/300x200?text=Медовик',
        ingredients: 'Мед, мука, сметана, сахар'
      }
    ],
  
    // Компоненты для конструктора
    components: {
      layers: [
        { id: 1, name: 'Шоколадный корж', price_per_unit: 300, type: 'layer' },
        { id: 2, name: 'Ванильный корж', price_per_unit: 250, type: 'layer' },
        { id: 3, name: 'Медовый корж', price_per_unit: 280, type: 'layer' },
        { id: 4, name: 'Кокосовый корж', price_per_unit: 320, type: 'layer' }
      ],
      creams: [
        { id: 1, name: 'Сливочный крем', price_per_unit: 200, type: 'cream' },
        { id: 2, name: 'Шоколадный крем', price_per_unit: 250, type: 'cream' },
        { id: 3, name: 'Сырный крем', price_per_unit: 300, type: 'cream' },
        { id: 4, name: 'Ягодный крем', price_per_unit: 280, type: 'cream' }
      ],
      fillings: [
        { id: 1, name: 'Клубничное варенье', price_per_unit: 150, type: 'filling' },
        { id: 2, name: 'Шоколадная крошка', price_per_unit: 100, type: 'filling' },
        { id: 3, name: 'Орехи грецкие', price_per_unit: 180, type: 'filling' },
        { id: 4, name: 'Карамельная начинка', price_per_unit: 200, type: 'filling' }
      ],
      decorations: [
        { id: 1, name: 'Шоколадная глазурь', price_per_unit: 120, type: 'decoration' },
        { id: 2, name: 'Свежие ягоды', price_per_unit: 200, type: 'decoration' },
        { id: 3, name: 'Цветы из крема', price_per_unit: 250, type: 'decoration' },
        { id: 4, name: 'Фруктовое ассорти', price_per_unit: 300, type: 'decoration' }
      ]
    },
  
    // Заказы
    orders: [
      {
        id: 1,
        order_date: '2024-12-01T14:30:00Z',
        total_amount: 2500,
        status: 'pending',
        delivery_type: 'delivery',
        delivery_address: 'ул. Примерная, д. 1, кв. 1',
        quantity: 1,
        cake: { id: 1, name: 'Шоколадный торт' }
      },
      {
        id: 2,
        order_date: '2024-11-28T10:15:00Z',
        total_amount: 5200,
        status: 'confirmed',
        delivery_type: 'pickup',
        quantity: 2,
        cake: { id: 2, name: 'Клубничный торт' }
      },
      {
        id: 3,
        order_date: '2024-11-25T16:45:00Z',
        total_amount: 3800,
        status: 'delivered',
        delivery_type: 'delivery',
        delivery_address: 'ул. Другая, д. 5',
        quantity: 1,
        custom_cake: { id: 101, name: 'Мой кастомный торт' }
      }
    ],
  
    // Кастомные торты
    customCakes: [
      {
        id: 101,
        name: 'Мой кастомный торт',
        layers: [
          { id: 1, name: 'Шоколадный корж', quantity: 2 }
        ],
        cream: { id: 1, name: 'Сливочный крем' },
        fillings: [
          { id: 2, name: 'Шоколадная крошка' }
        ],
        decorations: [
          { id: 1, name: 'Шоколадная глазурь' }
        ],
        total_price: 3800,
        weight: 1800
      }
    ]
  }