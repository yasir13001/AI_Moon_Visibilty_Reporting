import './ResponseMessage.css';

function ResponseMessage({ message, isError }) {
  return (
    <p className={isError ? "response-error" : "response-message"}>
      {message}
    </p>
  );
}

export default ResponseMessage;
