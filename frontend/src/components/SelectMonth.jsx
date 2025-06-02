import './SelectMonth.css';

function SelectMonth({ value, onChange }) {
  const islamicMonths = [
    "MUHARRAM",
    "SAFAR",
    "RABI-UL-AWWAL",
    "RABI-US-SANI",
    "JAMADI-UL-AWWAL",
    "JAMADI-US-SANI",
    "RAJAB",
    "SHABAN",
    "RAMADAN",
    "SHAWWAL",
    "ZUL-QADAH",
    "ZUL-HIJJAH"
  ];

  return (
    <div className="select-month">
      <label htmlFor="month">Islamic Month:</label>
      <select id="month" value={value} onChange={onChange} required>
        <option value="">--Select Month--</option>
        {islamicMonths.map(month => (
          <option key={month} value={month}>{month}</option>
        ))}
      </select>
    </div>
  );
}

export default SelectMonth;
