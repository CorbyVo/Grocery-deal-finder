import { useState } from "react";
import { compareDeals, type CompareResponse } from "./api";

function App() {
  const [shoppingListText, setShoppingListText] = useState("egg\npasta\nspaghetti");
  const [latitude, setLatitude] = useState(47.8560);
  const [longitude, setLongitude] = useState(12.1220);
  const [result, setResult] = useState<CompareResponse | null>(null);
  const [error, setError] = useState("");

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
    } catch (err) {
      setError("Could not connect to FastAPI backend.");
    }
  }

  return (
    <main style={{ padding: "32px", maxWidth: "1000px", margin: "0 auto" }}>
      <h1>Grocery Deal Finder</h1>

      <p>Compare supermarket offers and find the cheapest and nearest store.</p>

      <section>
        <h2>Shopping List</h2>

        <textarea
          value={shoppingListText}
          onChange={(e) => setShoppingListText(e.target.value)}
          rows={8}
          style={{ width: "100%", padding: "12px" }}
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

        <br />

        <label>
          Longitude:
          <input
            type="number"
            value={longitude}
            onChange={(e) => setLongitude(Number(e.target.value))}
            step="0.000001"
          />
        </label>

        <br />
        <br />

        <button onClick={handleCompare}>Compare</button>
      </section>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <section>
          <h2>Matched Products</h2>

          <table border={1} cellPadding={8}>
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

          <h2>Store Comparison</h2>

          {result.store_comparison && (
            <table border={1} cellPadding={8}>
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
          )}

          <h2>Recommendation</h2>
          <p>{result.message}</p>
        </section>
      )}
    </main>
  );
}

export default App;