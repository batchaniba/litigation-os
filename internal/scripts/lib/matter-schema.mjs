import { z } from "zod";

/** Zod schema for internal/src/data/matters/NN.json — the canonical matter record. */
export const MatterDocumentSchema = z.object({
  path: z.string().startsWith("/documents/"),
});

export const MatterCourtListenerSchema = z.object({
  court_id: z.string(),
  docket_id: z.number(),
  docket_url: z.string(),
}).partial();

export const MatterSchema = z.object({
  number: z.number().int().positive(),
  caption: z.string().min(1),
  case_no: z.string(),
  court: z.string().min(1),
  courtlistener: MatterCourtListenerSchema.optional(),
  claims: z.string(),
  status: z.string(),
  status_label: z.string(),
  lifecycle: z.string(),
  proceeding: z.string(),
  phase: z.string(),
  filed: z.string(),
  judge: z.string(),
  cluster: z.number().int(),
  type: z.string(),
  defendants: z.string(),
  archived: z.boolean(),
  badge: z.string(),
  causes: z.array(z.string()),
  key_facts: z.string(),
  procedural_status: z.string(),
  damages: z.string(),
  risk: z.string(),
  evidence: z.array(z.string()),
  documents: z.array(MatterDocumentSchema),
});

/** Validate a parsed matter JSON; returns an array of human-readable issues (empty = valid). */
export function validateMatter(data) {
  const result = MatterSchema.safeParse(data);
  if (result.success) return [];
  return result.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`);
}
