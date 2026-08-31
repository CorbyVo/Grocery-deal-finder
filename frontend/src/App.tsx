import { useState } from "react";
import { compareDeals, type CompareResponse, askProject } from "./api";
import "./App.css";

function App() {
  const [shoppingListText, setShoppingListText] = useState("egg\npasta\nspaghetti");
  const [latitude, setLatitude] = useState(47.8560);
  const [longitude, setLongitude] = useState(12.1220);
  const [result, setResult] = useState<CompareResponse | null>(null);
  const [error, setError] = useState("");
  const [projectQuestion, setProjectQuestion] = useState("");
  const [chatMessages, setChatMessages] = useState<
  { role: "user" | "assistant"; content: string }[]
>([]);

  async function handleCompare() {
    setError("");
    setResult(null);
    const shoppingList = shoppingListText
      .split("\n")
      .map((item) => item.trim())
      .filter((item) => item.length > 0);
    try {
      const data = await compareDeals({
        shopping_list: shoppingList,
        latitude,
        longitude,
        threshold: 0.5,
      });
      setResult(data);
    } catch {
      setError("Could not connect to FastAPI backend.");
    }
  }

  async function handleAskProject() {
  const question = projectQuestion.trim();
  if (!question) {return;}
  setChatMessages((prev) => [
    ...prev,
    { role: "user", content: question },
  ]);
  setProjectQuestion("");
  try {
    const data = await askProject(question);
    setChatMessages((prev) => [
      ...prev,
      { role: "assistant", content: data.answer },
    ]);
  } catch {
    setChatMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "Could not connect to the project assistant API.",
      },
    ]);
  }
}

return (
  <main className="app">
    <section className="hero">
      <h1>Grocery Deal Finder</h1>
      <p>Compare supermarket offers and find the cheapest and nearest store.</p>
    </section>

    <section className="grid">
      <section className="card">
        <h2>Shopping List</h2>

        <textarea
          value={shoppingListText}
          onChange={(e) => setShoppingListText(e.target.value)}
          rows={8}
        />

        <h2>Your Location</h2>

        <label>
          Latitude:
          <input
            type="number"
            value={latitude}
            onChange={(e) => setLatitude(Number(e.target.value))}
            step="0.000001"
          />
        </label>

        <label>
          Longitude:
          <input
            type="number"
            value={longitude}
            onChange={(e) => setLongitude(Number(e.target.value))}
            step="0.000001"
          />
        </label>

        <button onClick={handleCompare}>Compare</button>

        {error && <p className="error">{error}</p>}
      </section>

      <section className="card">
        <h2>Project Q&A Assistant</h2>
        <p>Ask how the project works, its limitations, or next steps.</p>

        <div className="chat-box">
          {chatMessages.map((message, index) => (
            <div key={index} className={`chat-message ${message.role}`}>
              <strong>{message.role === "user" ? "You" : "Assistant"}</strong>
              <p>{message.content}</p>
            </div>
          ))}
        </div>

        <div className="chat-input-row">
          <input
            value={projectQuestion}
            onChange={(e) => setProjectQuestion(e.target.value)}
            placeholder="Ask about this project..."
          />

          <button onClick={handleAskProject}>Ask</button>
        </div>
      </section>
    </section>

    {result && (
      <section className="card">
        <h2>Matched Products</h2>

        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>User Input</th>
                <th>Matched Product</th>
                <th>Confidence</th>
                <th>Method</th>
              </tr>
            </thead>

            <tbody>
              {result.matched_details.map((item, index) => (
                <tr key={index}>
                  <td>{item.user_input}</td>
                  <td>{item.matched_product}</td>
                  <td>{item.confidence}</td>
                  <td>{item.method}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <h2>Store Comparison</h2>

        {result.store_comparison && (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Store</th>
                  <th>Basket Total</th>
                  <th>Distance</th>
                  <th>Matched Items</th>
                  <th>Unmatched Items</th>
                </tr>
              </thead>

              <tbody>
                {result.store_comparison.map((store) => (
                  <tr key={store.store_id}>
                    <td>{store.store_name}</td>
                    <td>€{store.basket_total.toFixed(2)}</td>
                    <td>{store.distance_km.toFixed(2)} km</td>
                    <td>
                      {store.matched_items} / {store.requested_items}
                    </td>
                    <td>
                      {store.unmatched_items.length > 0
                        ? store.unmatched_items.join(", ")
                        : "None"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <h2>Recommendation</h2>
        <div className="success-box">{result.message}</div>
      </section>
    )}
  </main>
);
}

export default App;