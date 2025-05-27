import { describe, it, expect, vi, beforeEach } from 'vitest'
import * as api from '../lib/api'

describe('api.ts', () => {
  // Before each test, restore any mocks to their original behavior
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('fetchArticles calls fetch and returns JSON', async () => {
    // Prepare a fake response payload
    const mockData = { data: [{ id: 1, title: 'Test Article' }] }
    // Stub the global fetch function to return a resolved promise with our fake data
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData)
    }))

    // Call the function under test
    const result = await api.fetchArticles()
    // Assert fetch was called with the correct URL and credentials
    expect(fetch).toHaveBeenCalledWith('/api/ucdavis-news', { credentials: 'include' })
    // Assert the function returns the exact JSON we stubbed
    expect(result).toEqual(mockData)
  })

  it('fetchComments calls fetch with article_id', async () => {
    const aid = '123'
    const mockData = { data: [] } // empty list response

    // Stub fetch similarly
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData)
    }))

    // Call fetchComments with our sample ID
    const result = await api.fetchComments(aid)
    // Verify URL includes the correct query parameter
    expect(fetch).toHaveBeenCalledWith(`/api/comments?article_id=${aid}`, { credentials: 'include' })
    // And that we got back our mock data
    expect(result).toEqual(mockData)
  })

  it('postComment calls fetch with POST and returns JSON', async () => {
    const aid = '321'
    const content = 'Hello'
    const mockData = { id: '1', content }
    // Stub fetch to simulate POST
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData)
    }))

    // Call postComment
    const result = await api.postComment(aid, content)
    // Check fetch was called with the correct options
    expect(fetch).toHaveBeenCalledWith('/api/comments', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ article_id: aid, content })
    })
    // And returns the stubbed JSON
    expect(result).toEqual(mockData)
  })

  it('deleteComment calls fetch with DELETE', async () => {
    const cid = '987'
    // Stub fetch to simulate a successful DELETE
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true }))
    // Call deleteComment
    await api.deleteComment(cid)
    // Verify fetch used the correct HTTP method and URL
    expect(fetch).toHaveBeenCalledWith(`/api/comments/${cid}`, { method: 'DELETE', credentials: 'include' })
  })
})
