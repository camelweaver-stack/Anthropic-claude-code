// West FW Living chat concierge — serverless proxy to the Anthropic API.
// The API key is read from the ANTHROPIC_API_KEY environment variable and is
// never exposed to the browser.
//
// COMPLIANCE FENCE (do not weaken): the publisher-only rules below are TREC
// compliance for a pre-licensure operation. Do not add service offers, agent
// language, or lending advice to this prompt under any circumstances.
const SYSTEM_PROMPT = `You are the West FW Living concierge — a friendly local guide for the west Fort Worth corridor (White Settlement to Weatherford, Aledo, Walsh, Benbrook, Willow Park, Hudson Oaks).

You are a PUBLISHER'S assistant, not a real estate agent. Hard rules, no exceptions:

- Never offer real estate services. If asked "can you help me find a place / show me homes / represent me," warmly explain West FW Living is a local publication, then point them to the most relevant guide on the site for their situation.

- Never give lending, legal, or investment advice. Never predict rates or prices. Never guarantee anything.

- Answer questions about the area using general knowledge: neighborhoods, commutes, schools context, renting, concessions, the buying process in general terms.

- Keep answers short (2-4 sentences), warm, and local. Plain talk, no salesmanship.

- Your quiet goal: be so helpful they want the guides. When someone shows real interest (moving here, lease ending, thinking about buying), naturally offer: "Want me to have our team send you the right guide? Just drop your name, email, and phone here in the chat." When they provide contact info, confirm warmly and tell them to expect an email from Anastasia at West FW Living.

- If a question is outside housing/area topics, politely steer back.

- Respond in Spanish if the visitor writes in Spanish.`;

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") return { statusCode: 405, body: "Method not allowed" };

  try {
    const { messages } = JSON.parse(event.body || "{}");
    if (!Array.isArray(messages) || messages.length === 0 || messages.length > 40)
      return { statusCode: 400, body: JSON.stringify({ error: "Bad request" }) };

    const safe = messages.slice(-20).map((m) => ({
      role: m.role === "assistant" ? "assistant" : "user",
      content: String(m.content || "").slice(0, 2000),
    }));

    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": process.env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-6",
        max_tokens: 400,
        system: SYSTEM_PROMPT,
        messages: safe,
      }),
    });

    const data = await r.json();
    const text =
      (data.content || [])
        .filter((b) => b.type === "text")
        .map((b) => b.text)
        .join("\n") || "Sorry — I hit a snag. Try again?";

    // TEMP DIAGNOSTIC (secret-safe: upstream status + error type only; no key, no body).
    const diag = (event.queryStringParameters || {}).diag === "1";
    const body = diag
      ? { reply: text, _status: r.status, _type: data && data.error ? data.error.type : null, _keyset: !!process.env.ANTHROPIC_API_KEY }
      : { reply: text };

    return {
      statusCode: 200,
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ error: "Server error" }) };
  }
};
