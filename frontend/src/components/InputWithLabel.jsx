import './InputWithLabel.css';

function InputWithLabel({ label, id, type = "text", value, onChange }) {
  return (
    <div className="input-container">
      <label htmlFor={id}>{label}</label>
      <input id={id} type={type} value={value} onChange={onChange} required />
    </div>
  );
}

export default InputWithLabel;
