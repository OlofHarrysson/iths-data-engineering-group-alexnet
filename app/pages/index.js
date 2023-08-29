import React, { useState } from 'react';
import jsonData from "../../data/data_warehouse/Explain like i'm five/9b3fc437-d1ce-5ad5-b8a6-1de70da8010e_Explain_like_i'm_five.json";

function Header({ title }) {
  return <h1>{title ? title : 'Default title'}</h1>;
}

export default function HomePage() {
  const names = ['Alice', 'is', 'SIMPIN'];
  const [likes, setLikes] = useState(0);

  function handleClick() {
    setLikes(likes + 1);
  }

  return (
    <div>
      <Header title="Alexnet Daeshboard" />
      <ul>
        {names.map((name) => (
          <li key={name}>{name}</li>
        ))}
      </ul>


      <div>
        <h2>{jsonData.type_of_summary}</h2>
        <p>{jsonData.summary}</p>
      </div>
      <button onClick={handleClick}>Like ({likes})</button>
    </div>

  );
}