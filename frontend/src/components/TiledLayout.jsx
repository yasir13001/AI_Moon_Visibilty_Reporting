import React from 'react';
import './TiledLayout.css';

const items = [
  { id: 1, title: 'Item 1', description: 'Details of the first item' },
  { id: 2, title: 'Item 2', description: 'Details of the second item' },
  { id: 3, title: 'Item 3', description: 'Details of the third item' },
  { id: 4, title: 'Item 4', description: 'Details of the fourth item' },
 ];

const TiledLayout = () => {
  return (
    <div className="tiled-layout">
      {items.map((item) => (
        <div key={item.id} className="tile">
          <h3>{item.title}</h3>
          <p>{item.description}</p>
        </div>
      ))}
    </div>
  );
};

export default TiledLayout;
