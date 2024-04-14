import React, { useState } from "react";
import "./cashback.css";
import { Link } from "react-router-dom";
import NavBar from "./nav";

function CashBackPage() {
  return (
    <div>
      <NavBar />
      <form action="" className="cashback_form">
        <div className="input-group">
          <label>Категория: </label>
          <select name="" id="" required>
            <option value="telephony">Телефоны и гаджеты</option>
            <option value="computers">Компьютеры</option>
            <option value="kids">Детские товары</option>
            <option value="beauty">Красота и здоровье</option>
            <option value="accessories">Аксессуары</option>
            <option value="jewelry">Украшения</option>
            <option value="home">Товары для дома и дачи</option>
            <option value="furniture">Мебель</option>
            <option value="building">Строительство и ремонт</option>
            <option value="chancery">Канцелярские товары</option>
            <option value="products">Продукты</option>
            <option value="health">Аптека</option>
            <option value="tech">ТВ, аудио, видео</option>
            <option value="tech">Бытовая техника</option>
            <option value="auto">Автотовары</option>
            <option value="sport">Спорт и туризм</option>
            <option value="shoes">Обувь</option>
            <option value="clothes">Одежда</option>
            <option value="entertainment">Досуг и книги</option>
            <option value="animals">Товары для животных</option>
            <option value="celebration">Подарки и товары для праздников</option>
          </select>
        </div>
        <div className="input-group">
          <label>Сумма оплаты: </label>
          <input type="text" required/>
        </div>
        <button type="submit">Search</button>
      </form>
    </div>
  );
}

export default CashBackPage;
