import './ButtonGroup.css';

function ButtonGroup({ onGenerateMoonParameters, onGenerateVisibilityReport }) {
  return (
    <div className="btn-class">
      <button type="button" onClick={onGenerateMoonParameters}>
        Generate Moon Parameters
      </button>
      <button type="button" onClick={onGenerateVisibilityReport}>
        Generate Visibility Report
      </button>
    </div>
  );
}

export default ButtonGroup;
