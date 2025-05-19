import { render, screen } from '@testing-library/svelte'
import Header from '../Header.svelte'

// (Optional) add data-testids inside your components for easier targeting.

describe('Header.svelte', () => {
  it('mounts Top, Logo and Categories', () => {
    render(Header)
    // If you added data-testid attributes:
    expect(screen.getByTestId('top')).toBeInTheDocument()
    expect(screen.getByTestId('logo')).toBeInTheDocument()
    // Categories has a “News” button by default?
    expect(screen.getByText('News')).toBeInTheDocument()
  })
})
