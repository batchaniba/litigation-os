import { describe, expect, it, vi } from "vitest";
import { isCapacityError, retryOnCapacity } from "./retry.mjs";

describe("isCapacityError", () => {
  it("matches the Cloudflare max_instances error", () => {
    expect(isCapacityError(new Error("Maximum number of running container instances exceeded"))).toBe(
      true,
    );
    expect(isCapacityError("maximum number of running container instances exceeded.")).toBe(true);
    expect(isCapacityError(new Error("no instance available"))).toBe(false);
  });
});

describe("retryOnCapacity", () => {
  it("returns on the first success", async () => {
    const fn = vi.fn(async () => "ok");
    await expect(retryOnCapacity(fn, { delays: [0, 5], sleep: async () => {} })).resolves.toBe("ok");
    expect(fn).toHaveBeenCalledOnce();
  });

  it("retries capacity errors and then succeeds", async () => {
    const slept = [];
    const fn = vi
      .fn()
      .mockRejectedValueOnce(new Error("Maximum number of running container instances exceeded"))
      .mockResolvedValueOnce("started");
    await expect(
      retryOnCapacity(fn, {
        delays: [0, 25],
        sleep: async (ms) => {
          slept.push(ms);
        },
      }),
    ).resolves.toBe("started");
    expect(fn).toHaveBeenCalledTimes(2);
    expect(slept).toEqual([25]);
  });

  it("does not retry unrelated errors", async () => {
    const fn = vi.fn(async () => {
      throw new Error("port not ready");
    });
    await expect(retryOnCapacity(fn, { delays: [0, 5], sleep: async () => {} })).rejects.toThrow(
      "port not ready",
    );
    expect(fn).toHaveBeenCalledOnce();
  });

  it("throws the last capacity error after the delays are exhausted", async () => {
    const fn = vi.fn(async () => {
      throw new Error("Maximum number of running container instances exceeded");
    });
    await expect(retryOnCapacity(fn, { delays: [0, 0], sleep: async () => {} })).rejects.toThrow(
      /maximum number of running container instances exceeded/i,
    );
    expect(fn).toHaveBeenCalledTimes(2);
  });
});
