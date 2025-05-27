import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/svelte'
import '@testing-library/jest-dom'
import App from '../App.svelte'

describe('App.svelte', () => {
  it('mounts without crashing', () => {
    // Render the App component into JSDOM
    const { container } = render(App)
    // The container element should now exist in the document
    expect(container).toBeInTheDocument()
  })
})
