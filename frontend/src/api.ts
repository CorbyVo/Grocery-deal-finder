export type CompareRequest = {
  shopping_list: string[];
  latitude: number;
  longitude: number;
  threshold: number;
};

export type MatchedDetail = {
  user_input: string;
  matched_product: string;
  similarity_score: number;
  confidence: string;
  method: string;
};

export type StoreComparison = {
  store_id: number;
  store_name: string;
  basket_total: number;
  distance_km: number;
  requested_items: number;
  matched_items: number;
  unmatched_items: string[];
};

export type CompareResponse = {
  matched_details: MatchedDetail[];
  unmatched_user_inputs: string[];
  store_comparison: StoreComparison[] | null;
  message: string;
};

const API_BASE_URL = "http://127.0.0.1:8000";

export async function compareDeals(
  payload: CompareRequest
): Promise<CompareResponse> {
  const response = await fetch(`${API_BASE_URL}/compare`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error("Failed to compare grocery deals.");
  }
  return response.json();
}

export type ProjectChatResponse = {
  answer: string;
  sources: {
    source: string;
    score: number;
  }[];
};

export async function askProject(question: string): Promise<ProjectChatResponse> {
  const response = await fetch(`${API_BASE_URL}/project-chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });
  if (!response.ok) {
    throw new Error("Failed to ask project assistant.");
  }
  return response.json();
}